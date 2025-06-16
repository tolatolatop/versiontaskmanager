from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, ResultViewSet, TaskResultViewSet
from .views import VersionViewSet, ManifestViewSet, VersionConfigViewSet
from .views import TaskTriggerView, TaskStatusView

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'results', ResultViewSet)
router.register(r'task-results', TaskResultViewSet)
router.register(r'versions', VersionViewSet)
router.register(r'manifests', ManifestViewSet)
router.register(r'version-configs', VersionConfigViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('tasks/trigger/', TaskTriggerView.as_view(), name='task-trigger'),
    path('tasks/status/<str:task_id>/',
         TaskStatusView.as_view(), name='task-status'),
]
