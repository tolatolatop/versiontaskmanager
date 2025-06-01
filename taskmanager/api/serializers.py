from rest_framework import serializers
from .models import Task, Result, TaskResult
from .models import Version, Manifest, VersionConfig


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


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = ['id', 'product_id', 'version_name',
                  'version_description', 'version_created_at', 'version_updated_at']
        read_only_fields = ['version_created_at', 'version_updated_at']


class ManifestSerializer(serializers.ModelSerializer):
    version = serializers.PrimaryKeyRelatedField(
        queryset=Version.objects.all())

    class Meta:
        model = Manifest
        fields = ['id', 'version', 'repo_url', 'repo_revision',
                  'manifest_filepath', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class VersionConfigSerializer(serializers.ModelSerializer):
    version = serializers.PrimaryKeyRelatedField(
        queryset=Version.objects.all())

    class Meta:
        model = VersionConfig
        fields = ['id', 'version', 'data', 'created_at', 'updated_at']
