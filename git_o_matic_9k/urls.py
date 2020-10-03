from django.urls import include, path
from django.shortcuts import redirect


urlpatterns = [
    path('', lambda _: redirect('github/')),
    path('github/', include('github.urls')),
    path('health/', include('health.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
