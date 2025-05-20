from rest_framework import serializers
from .models import Task, Result, TaskResult


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ['id', 'status', 'result_data', 'error_message',
                  'execution_time', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    results = ResultSerializer(
        many=True, read_only=True, source='task_results.result')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status',
                  'created_at', 'updated_at', 'owner', 'results']
        read_only_fields = ['created_at', 'updated_at']


class TaskResultSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    result = ResultSerializer()

    class Meta:
        model = TaskResult
        fields = ['id', 'task', 'result', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        result_data = validated_data.pop('result')
        result = Result.objects.create(**result_data)
        task_result = TaskResult.objects.create(
            result=result, **validated_data)
        return task_result
