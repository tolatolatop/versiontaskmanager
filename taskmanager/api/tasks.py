from background_task import background
from datetime import datetime


@background(schedule=60)  # 每60秒执行一次
def example_task():
    """
    示例后台任务
    """
    print(f"后台任务执行时间: {datetime.now()}")
    # 在这里添加您的任务逻辑
