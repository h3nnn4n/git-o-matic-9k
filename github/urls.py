from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'developers', views.DeveloperViewSet)
router.register(r'repositories', views.RepositoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
