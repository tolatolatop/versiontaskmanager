from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task, TaskResult
from .serializers import TaskSerializer, TaskResultSerializer

# Create your views here.


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        task = serializer.save(owner=self.request.user)
        # 创建关联的任务结果
        TaskResult.objects.create(task=task)

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
