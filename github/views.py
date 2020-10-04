from django.http import HttpResponse, Http404
from rest_framework import viewsets
from rest_framework import permissions, response

from .models import Developer, Repository, RateLimit
from .serializers import DeveloperSerializer, RepositorySerializer
from .serializers import RateLimitSerializer, TaskSerializer
from .enumerations import TASKS
from . import tasks


class DeveloperViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for developers (github users)
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
    """
    Endpoint for triggering a full sync of a developer. This updates the
    developer record, the followers and following lists, starred repositories,
    fetches all of the developer's repositories and its stargazer.
    """
    if request.user.is_authenticated:
        print('authenticated user')
    else:
        print('not authenticated user')

    tasks.full_profile_sync.delay(username)

    return HttpResponse('ok')


def repository_sync(request, username, repository):
    """
    Endpoint for triggering a full sync of a repository. This fetches and
    updates the repository and its owner. Stargazers are also created and
    updated.
    """
    if request.user.is_authenticated:
        print('authenticated user')
    else:
        print('not authenticated user')

    repo_full_name = '/'.join([username, repository])
    tasks.add_or_update_repository.delay(repo_full_name, populate_stargazers=True)

    return HttpResponse('ok')


def discovery_scraper(request):
    """
    Triggers the discovery scrapper. This by default picks 5 users where the
    following, followers or repository count if out of date and runs a full
    sync.
    """
    if not request.user.is_authenticated:
        return Http404()

    tasks.discovery_scraper.delay()

    return HttpResponse('ok')

class TasksView(viewsets.ViewSet):
    """
    Endpoint for listing tasks and triggering them
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *_args, **_kwargs): # pylint: disable=too-many-return-statements
        """
        Triggers an actions
        """
        task_name = request.POST.get('name')
        username = request.POST.get('username')
        repo_name = request.POST.get('repo_name')

        if task_name == 'full_profile_sync':
            if username == '':
                return response.Response(
                    {'success': 'no', 'error': 'Missing username. Provide a valid github username'},
                    status=406
                )

            tasks.full_profile_sync.delay(username)
            return response.Response({'success': 'yes'})

        if task_name == 'full_repository_sync':
            if username == '':
                return response.Response(
                    {'success': 'no', 'error': 'Missing username. Provide a valid github username'},
                    status=406
                )

            if repo_name == '':
                return response.Response(
                    {'success': 'no', 'error': 'Missing repo_name. Provide a valid repository name'},
                    status=406
                )

            tasks.add_or_update_repository.delay('/'.join([username, repo_name]), populate_stargazers=True)
            return response.Response({'success': 'yes'})

        if task_name == 'discovery_scraper':
            if username == '':
                return response.Response(
                    {'success': 'no', 'error': 'Missing username. Provide a valid github username'},
                    status=406
                )

            tasks.discovery_scraper.delay()
            return response.Response({'success': 'yes'})

        return response.Response(
            {'success': 'no', 'error': f'task name {task_name} not recognized'},
            status=406
        )

    def list(self, _request):
        """
        Lists the available actions
        """
        serializer = TaskSerializer(instance=TASKS.values(), many=True)
        return response.Response(serializer.data)

    # Not sure if this is a good idea or not. But it works
    @classmethod
    def get_extra_actions(cls):
        return []
