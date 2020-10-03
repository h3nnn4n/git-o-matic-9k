from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'developers', views.DeveloperViewSet)
router.register(r'repositories', views.RepositoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('developers/trigger_sync/<str:username>/',
         views.full_developer_sync,
         name='full_developer_sync'),
    path('repositories/trigger_sync/<str:username>/<str:repository>/',
         views.repository_sync,
         name='repository_sync'),
]
