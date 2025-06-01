from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', '待处理'),
        ('in_progress', '进行中'),
        ('completed', '已完成'),
    ]

    title = models.CharField(max_length=200, verbose_name='标题')
    description = models.TextField(blank=True, verbose_name='描述')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='状态'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name='创建者'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = '任务'
        verbose_name_plural = '任务'

    def __str__(self):
        return self.title


class Result(models.Model):
    RESULT_STATUS_CHOICES = [
        ('success', '成功'),
        ('failed', '失败'),
        ('error', '错误'),
    ]

    status = models.CharField(
        max_length=20,
        choices=RESULT_STATUS_CHOICES,
        default='success',
        verbose_name='结果状态'
    )
    result_data = models.JSONField(
        default=dict,
        verbose_name='结果数据'
    )
    error_message = models.TextField(
        blank=True,
        verbose_name='错误信息'
    )
    execution_time = models.FloatField(
        null=True,
        blank=True,
        verbose_name='执行时间(秒)'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = '结果'
        verbose_name_plural = '结果'

    def __str__(self):
        return f"Result {self.id} - {self.status}"


class TaskResult(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='task_results',
        verbose_name='任务'
    )
    result = models.ForeignKey(
        Result,
        on_delete=models.CASCADE,
        related_name='task_results',
        verbose_name='结果'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = '任务结果关联'
        verbose_name_plural = '任务结果关联'
        unique_together = ['task', 'result']

    def __str__(self):
        return f"Task {self.task.id} - Result {self.result.id}"


class Version(models.Model):
    product_id = models.CharField(max_length=200, verbose_name='产品ID')
    version_name = models.CharField(max_length=200, verbose_name='版本名称')
    version_description = models.TextField(blank=True, verbose_name='版本描述')
    version_created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='创建时间')
    version_updated_at = models.DateTimeField(
        auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['-version_created_at']
        verbose_name = '版本'
        verbose_name_plural = '版本'


class Manifest(models.Model):
    version = models.ForeignKey(
        Version,
        on_delete=models.CASCADE,
        related_name='manifests',
        verbose_name='版本'
    )
    repo_url = models.CharField(max_length=200, verbose_name='仓库URL')
    repo_revision = models.CharField(max_length=200, verbose_name='仓库版本')
    manifest_filepath = models.CharField(
        max_length=200, verbose_name='清单文件路径')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '清单'
        verbose_name_plural = '清单'


class VersionConfig(models.Model):
    version = models.ForeignKey(
        Version,
        on_delete=models.CASCADE,
        related_name='configs',
        verbose_name='版本'
    )
    data = models.JSONField(default=dict, verbose_name='版本配置')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '版本配置'
        verbose_name_plural = '版本配置'

    def __str__(self):
        return f"VersionConfig {self.id} - {self.version.version_name}"
