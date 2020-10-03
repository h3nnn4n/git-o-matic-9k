from rest_framework import viewsets
from rest_framework import permissions

from .models import Developer, Repository
from .serializers import DeveloperSerializer, RepositorySerializer


class DeveloperViewSet(viewsets.ModelViewSet):
    """
    API endpoint for developers
    """
    queryset = Developer.objects.all().order_by('-created_at')
    serializer_class = DeveloperSerializer
    permission_classes = [permissions.IsAuthenticated]


class RepositoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for repositories
    """
    queryset = Repository.objects.all().order_by('-created_at')
    serializer_class = RepositorySerializer
    permission_classes = [permissions.IsAuthenticated]
