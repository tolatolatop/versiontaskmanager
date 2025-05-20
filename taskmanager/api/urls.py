from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, ResultViewSet, TaskResultViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'results', ResultViewSet)
router.register(r'task-results', TaskResultViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
