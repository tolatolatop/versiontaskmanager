#!/usr/bin/env python3
import requests
import time
import json
import logging
from typing import Dict, Any
from datetime import datetime

# 配置日志


def setup_logger():
    logger = logging.getLogger('CeleryTaskTester')
    logger.setLevel(logging.DEBUG)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # 创建文件处理器
    file_handler = logging.FileHandler(
        f'celery_task_test_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)

    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # 添加处理器到日志记录器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


class CeleryTaskTester:
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
        self.session = requests.Session()
        self.logger = logging.getLogger('CeleryTaskTester')
        # 设置基本的请求头
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.logger.info(f"初始化 CeleryTaskTester，基础URL: {base_url}")

    def trigger_task(self, delay_seconds: int = 5) -> Dict[str, Any]:
        """
        触发一个新的Celery任务
        :param delay_seconds: 任务延迟执行的秒数
        :return: 任务信息
        """
        url = f"{self.base_url}/tasks/trigger/"
        data = {"delay_seconds": delay_seconds}

        self.logger.info(f"准备触发新任务，延迟时间: {delay_seconds}秒")
        self.logger.debug(f"请求URL: {url}")
        self.logger.debug(f"请求数据: {json.dumps(data, ensure_ascii=False)}")

        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            result = response.json()
            self.logger.info(
                f"任务触发成功: {json.dumps(result, ensure_ascii=False)}")
            return result
        except requests.exceptions.RequestException as e:
            self.logger.error(f"触发任务失败: {str(e)}", exc_info=True)
            return {}

    def check_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        检查任务状态
        :param task_id: 任务ID
        :return: 任务状态信息
        """
        url = f"{self.base_url}/tasks/status/{task_id}/"
        self.logger.debug(f"检查任务状态，任务ID: {task_id}")

        try:
            response = self.session.get(url)
            response.raise_for_status()
            result = response.json()
            self.logger.debug(
                f"任务状态响应: {json.dumps(result, ensure_ascii=False)}")
            return result
        except requests.exceptions.RequestException as e:
            self.logger.error(f"检查任务状态失败: {str(e)}", exc_info=True)
            return {}

    def monitor_task(self, task_id: str, interval: int = 1, timeout: int = 60) -> Dict[str, Any]:
        """
        监控任务直到完成或超时
        :param task_id: 任务ID
        :param interval: 检查间隔（秒）
        :param timeout: 超时时间（秒）
        :return: 最终任务状态
        """
        self.logger.info(
            f"开始监控任务 {task_id}，检查间隔: {interval}秒，超时时间: {timeout}秒")
        start_time = time.time()
        check_count = 0

        while True:
            check_count += 1
            status = self.check_task_status(task_id)
            self.logger.info(
                f"第 {check_count} 次检查 - 任务状态: {json.dumps(status, ensure_ascii=False)}")

            if status.get('status') in ['completed', 'failed']:
                self.logger.info(
                    f"任务 {task_id} 已完成，状态: {status.get('status')}")
                return status

            if time.time() - start_time > timeout:
                self.logger.warning(f"任务 {task_id} 监控超时（{timeout}秒）")
                return status

            time.sleep(interval)


def main():
    # 设置日志记录器
    logger = setup_logger()
    logger.info("开始执行Celery任务测试")

    try:
        # 创建测试器实例
        tester = CeleryTaskTester()

        # 触发一个10秒的任务
        logger.info("准备触发新任务...")
        task_info = tester.trigger_task(delay_seconds=10)
        logger.info(
            f"任务信息: {json.dumps(task_info, ensure_ascii=False, indent=2)}")

        if task_info:
            # 监控任务直到完成
            logger.info("开始监控任务...")
            final_status = tester.monitor_task(
                task_info['task_id'],
                interval=1,  # 每秒检查一次
                timeout=15   # 15秒超时
            )
            logger.info("任务最终状态:")
            logger.info(json.dumps(final_status, ensure_ascii=False, indent=2))
        else:
            logger.error("任务触发失败，无法继续监控")

    except Exception as e:
        logger.error(f"测试过程中发生错误: {str(e)}", exc_info=True)
    finally:
        logger.info("Celery任务测试结束")


if __name__ == "__main__":
    main()
