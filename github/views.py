from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions

from .models import Developer, Repository
from .serializers import DeveloperSerializer, RepositorySerializer
from .tasks import add_or_update_user, add_or_update_all_user_repositories, add_or_update_repository


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


def full_developer_sync(request, username):
    if request.user.is_authenticated:
        print('authenticated user')
    else:
        print('not authenticated user')

    add_or_update_user.delay(username)
    add_or_update_all_user_repositories.delay(username)

    return HttpResponse('ok')


def repository_sync(request, username, repository):
    if request.user.is_authenticated:
        print('authenticated user')
    else:
        print('not authenticated user')

    repo_full_name = '/'.join([username, repository])
    add_or_update_repository.delay(repo_full_name)

    return HttpResponse('ok')
