from celery import shared_task
import time
from datetime import datetime


@shared_task(name='api.tasks.simple_task')
def simple_task(task_id: str, delay_seconds: int = 5):
    """
    一个简单的Celery任务示例
    :param task_id: 任务ID
    :param delay_seconds: 延迟执行的秒数
    :return: 任务执行结果
    """
    # 模拟耗时操作
    time.sleep(delay_seconds)

    # 返回任务执行结果
    return {
        'task_id': task_id,
        'status': 'completed',
        'executed_at': datetime.now().isoformat(),
        'message': f'Task {task_id} completed after {delay_seconds} seconds'
    }
