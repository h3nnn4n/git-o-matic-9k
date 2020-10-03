from celery import shared_task

from .models import Developer, Repository
from . import github_api


@shared_task
def add_or_update_user(user_name):
    result = github_api.get_user(user_name)

    fields = [
        'login',
        'name',
        'location',
        'bio',
        'company',
        'email',

        'created_at',
        'updated_at',

        'followers',
        'following',
        'public_gists',
        'public_repos',
    ]

    defaults = { field: result[field] for field in fields }
    defaults['data_source'] = result

    Developer.objects.update_or_create(
        github_id=result['id'],
        defaults=defaults
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

    try:
        defaults['owner'] = Developer.objects.get(github_id=result['owner']['id'])
    except Developer.DoesNotExist:
        # If the user doesnt exist yet, create it
        user_name = repo_name.split('/')[0]
        add_or_update_user.run(user_name)
        defaults['owner'] = Developer.objects.get(github_id=result['owner']['id'])

    Repository.objects.update_or_create(
        github_id=result['id'],
        defaults=defaults
    )
