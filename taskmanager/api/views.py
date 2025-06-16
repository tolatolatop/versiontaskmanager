from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task, Result, TaskResult
from .models import Version, Manifest, VersionConfig
from .serializers import TaskSerializer, ResultSerializer, TaskResultSerializer
from .serializers import VersionSerializer, ManifestSerializer, VersionConfigSerializer
from rest_framework.views import APIView
from .tasks import simple_task
import uuid

# Create your views here.


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Result.objects.filter(task_results__task__owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskResultViewSet(viewsets.ModelViewSet):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TaskResult.objects.filter(task__owner=self.request.user)

    def perform_create(self, serializer):
        task_id = self.request.data.get('task')
        task = Task.objects.get(id=task_id, owner=self.request.user)
        serializer.save(task=task)

    @action(detail=True, methods=['post'])
    def update_result(self, request, pk=None):
        task = self.get_object()
        result = task.result
        serializer = TaskResultSerializer(
            result, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer
    permission_classes = []

    def get_queryset(self):
        return Version.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class ManifestViewSet(viewsets.ModelViewSet):
    queryset = Manifest.objects.all()
    serializer_class = ManifestSerializer

    def get_queryset(self):
        return Manifest.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class VersionConfigViewSet(viewsets.ModelViewSet):
    queryset = VersionConfig.objects.all()
    serializer_class = VersionConfigSerializer

    def get_queryset(self):
        return VersionConfig.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class TaskTriggerView(APIView):
    """
    用于触发Celery任务的API视图
    """

    def post(self, request):
        # 生成唯一的任务ID
        task_id = str(uuid.uuid4())

        # 从请求中获取延迟时间，默认为5秒
        delay_seconds = request.data.get('delay_seconds', 5)

        # 异步执行任务
        task = simple_task.delay(task_id, delay_seconds)

        return Response({
            'task_id': task_id,
            'celery_task_id': task.id,
            'status': 'pending',
            'message': f'Task {task_id} has been queued'
        }, status=status.HTTP_202_ACCEPTED)


class TaskStatusView(APIView):
    """
    用于查询任务状态的API视图
    """

    def get(self, request, task_id):
        from celery.result import AsyncResult

        # 获取Celery任务结果
        task_result = AsyncResult(task_id)

        if task_result.ready():
            if task_result.successful():
                return Response({
                    'task_id': task_id,
                    'status': 'completed',
                    'result': task_result.result
                })
            else:
                return Response({
                    'task_id': task_id,
                    'status': 'failed',
                    'error': str(task_result.result)
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'task_id': task_id,
                'status': 'pending',
                'message': 'Task is still running'
            })
