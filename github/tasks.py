from celery import shared_task

from . import services

from .models import Developer, Repository
from . import github_api


@shared_task
def add_or_update_user(user_name):
    dev_data = github_api.get_user(user_name)

    services.add_or_update_user(dev_data)


@shared_task
def add_or_update_repository(repo_name):
    repo_data = github_api.get_repository(repo_name)

    try:
        services.add_or_update_repository(repo_data)
    except Developer.DoesNotExist:
        # If the user doesnt exist yet, create it
        user_name = repo_name.split('/')[0]
        add_or_update_user.run(user_name)

    services.add_or_update_repository(repo_data)
