from django.contrib import admin
from .models import Task, Result, TaskResult


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'owner', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'owner')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'execution_time', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('error_message',)
    date_hierarchy = 'created_at'


@admin.register(TaskResult)
class TaskResultAdmin(admin.ModelAdmin):
    list_display = ('task', 'result', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('task__title', 'result__status')
    date_hierarchy = 'created_at'
