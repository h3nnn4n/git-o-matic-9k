from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'developers', views.DeveloperViewSet)
router.register(r'repositories', views.RepositoryViewSet)
router.register(r'rate_limit', views.RateLimitViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('developers/trigger_sync/<str:username>/',
         views.full_developer_sync,
         name='full_developer_sync'),
    path('repositories/trigger_sync/<str:username>/<str:repository>/',
         views.repository_sync,
         name='repository_sync'),
    path('trigger_discovery/',
         views.discovery_scraper,
         name='discovery_scraper'),
]
