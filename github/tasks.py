from celery import shared_task

from .models import Developer, Repository
from . import github_api


@shared_task
def add_or_update_user(user_name):
    result = github_api.get_user(user_name)

    Developer.objects.update_or_create(
        github_id=result['id'],
        defaults={
            'user_name': result['login'],
            'data_source': result,
        }
    )


@shared_task
def add_or_update_repository(repo_name):
    result = github_api.get_repository(repo_name)

    fields = [
        'name',
        'full_name',
        'description',
        'homepage',
        'language',
        'created_at',
        'updated_at',

        'has_downloads',
        'has_issues',
        'has_pages',
        'has_projects',
        'has_wiki',
        'private',
        'archived',
        'disabled',

        'stargazers_count',
        'subscribers_count',
        'watchers_count',
        'open_issues_count',
    ]

    defaults = { field: result[field] for field in fields }
    defaults['data_source'] = result

    Repository.objects.update_or_create(
        github_id=result['id'],
        defaults=defaults
    )
