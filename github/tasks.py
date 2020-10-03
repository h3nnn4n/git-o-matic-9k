from celery import shared_task

from . import services
from . import github_api

from .models import Developer


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


@shared_task
def add_or_update_all_user_repositories(user_name, next_page_link=None):
    all_repo_data, links = github_api.list_repositories(user_name, page_link=next_page_link)

    for repo_data in all_repo_data:
        add_or_update_repository.delay(repo_data['full_name'])

    if 'next' in links.keys():
        add_or_update_all_user_repositories(user_name, links['next'])
