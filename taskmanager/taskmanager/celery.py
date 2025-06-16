import os
from celery import Celery

# 设置Django默认设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskmanager.settings')

# 创建Celery实例
app = Celery('taskmanager')

# 使用Django的设置文件配置Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动从所有已注册的Django应用中加载任务
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
