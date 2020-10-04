from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers, permissions

from . import views

# pylint: disable=invalid-name
schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.IsAuthenticated,),
)

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
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
