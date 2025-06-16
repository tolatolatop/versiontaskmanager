from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Task
from django.contrib.auth.models import User
import json

# Create your tests here.


class TaskAPITestCase(TestCase):
    def setUp(self):
        """测试前的准备工作"""
        # 确保清理所有数据
        Task.objects.all().delete()
        User.objects.all().delete()

        self.client = APIClient()
        # 创建测试用户
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

        self.task_data = {
            'title': '测试任务',
            'description': '这是一个测试任务',
            'status': 'pending'
        }
        self.task_url = reverse('task-list')

    def tearDown(self):
        """测试后的清理工作"""
        Task.objects.all().delete()
        User.objects.all().delete()

    def test_create_task(self):
        """测试创建任务"""
        # 确保开始时没有任务
        self.assertEqual(Task.objects.count(), 0)

        response = self.client.post(
            self.task_url,
            data=json.dumps(self.task_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, '测试任务')

    def test_get_task_list(self):
        """测试获取任务列表"""
        # 确保开始时没有任务
        self.assertEqual(Task.objects.count(), 0)

        # 创建测试任务
        task = Task.objects.create(
            title=self.task_data['title'],
            description=self.task_data['description'],
            status=self.task_data['status'],
            owner=self.user
        )

        # 打印当前数据库中的所有任务
        print("\n当前数据库中的任务:")
        for t in Task.objects.all():
            print(f"ID: {t.id}, Title: {t.title}, Owner: {t.owner.username}")

        response = self.client.get(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 检查分页响应结构
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(response.data['count'], 1)  # 总数应该为1

        # 检查返回的任务数据
        task_data = response.data['results'][0]
        self.assertEqual(task_data['title'], self.task_data['title'])
        self.assertEqual(task_data['description'],
                         self.task_data['description'])
        self.assertEqual(task_data['status'], self.task_data['status'])
        self.assertEqual(task_data['owner'], self.user.username)
        self.assertEqual(task_data.get('results', []), [])  # 新创建的任务应该没有结果
