from rest_framework import serializers
from .models import Task, TaskResult


class TaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = ['id', 'status', 'result_data', 'error_message',
                  'execution_time', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    result = TaskResultSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status',
                  'created_at', 'updated_at', 'owner', 'result']
        read_only_fields = ['created_at', 'updated_at']
