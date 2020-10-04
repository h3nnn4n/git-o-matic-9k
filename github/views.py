from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework import permissions

from .models import Developer, Repository, RateLimit
from .serializers import DeveloperSerializer, RepositorySerializer, RateLimitSerializer
from .tasks import add_or_update_user, add_or_update_all_user_repositories, add_or_update_repository


class DeveloperViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for developers
    """
    queryset = Developer.objects.all().order_by('-created_at')
    serializer_class = DeveloperSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = {
        'login': ['exact', 'lte', 'gte'],
        'name': ['exact', 'lte', 'gte', 'isnull', 'contains'],
        'location': ['exact', 'lte', 'gte', 'isnull'],
        'bio': ['exact', 'lte', 'gte', 'isnull', 'contains'],
        'company': ['exact', 'lte', 'gte', 'isnull'],
        'email': ['exact', 'lte', 'gte', 'isnull'],
        'followers_count': ['exact', 'lte', 'gte'],
        'following_count': ['exact', 'lte', 'gte'],
        'public_gists': ['exact', 'lte', 'gte'],
        'public_repos': ['exact', 'lte', 'gte'],
        'created_at': ['exact', 'lte', 'gte'],
        'updated_at': ['exact', 'lte', 'gte'],
    }


class RepositoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for repositories
    """
    queryset = Repository.objects.all().order_by('-created_at')
    serializer_class = RepositorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = {
        'owner_github_id': ['exact'],
        'name': ['exact'],
        'full_name': ['exact'],
        'description': ['exact', 'isnull', 'contains'],
        'homepage': ['exact', 'isnull'],
        'language': ['exact', 'isnull'],
        'created_at': ['exact', 'lte', 'gte'],
        'updated_at': ['exact', 'lte', 'gte'],
        'has_downloads': ['exact'],
        'has_issues': ['exact'],
        'has_pages': ['exact'],
        'has_projects': ['exact'],
        'has_wiki': ['exact'],
        'private': ['exact'],
        'archived': ['exact'],
        'disabled': ['exact'],
        'stargazers_count': ['exact', 'lte', 'gte'],
        'subscribers_count': ['exact', 'lte', 'gte'],
        'watchers_count': ['exact', 'lte', 'gte'],
        'open_issues_count': ['exact', 'lte', 'gte'],
    }


class RateLimitViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for the github rate limiting quotas
    """
    queryset = RateLimit.objects.all()
    serializer_class = RateLimitSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = {
        'rate_limit': ['exact', 'lte', 'gte'],
        'rate_remaining': ['exact', 'lte', 'gte'],
        'rate_reset': ['exact', 'lte', 'gte'],
        'rate_reset_raw': ['exact', 'lte', 'gte'],
    }


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
