from celery import shared_task

from . import services
from . import github_api

from .models import Developer


@shared_task
def add_or_update_user(user_name):
    if not github_api.can_make_new_requests():
        add_or_update_user.apply_async(
            args=[user_name],
            eta=github_api.next_request_time(),
        )

        return

    dev_data = github_api.get_user(user_name)

    services.add_or_update_user(dev_data)


@shared_task
def add_or_update_repository(repo_name):
    if not github_api.can_make_new_requests():
        add_or_update_repository.apply_async(
            args=[repo_name],
            eta=github_api.next_request_time(),
        )

        return

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
    if not github_api.can_make_new_requests():
        add_or_update_all_user_repositories.apply_async(
            args=[user_name, next_page_link],
            eta=github_api.next_request_time(),
        )

        return

    all_repo_data, links = github_api.list_repositories(user_name, page_link=next_page_link)

    for repo_data in all_repo_data:
        add_or_update_repository.delay(repo_data['full_name'])

    if 'next' in links.keys():
        add_or_update_all_user_repositories(user_name, links['next'])


@shared_task
def add_or_update_user_followers(user_name, next_page_link=None):
    if not github_api.can_make_new_requests():
        add_or_update_user_followers.apply_async(
            args=[user_name, next_page_link],
            eta=github_api.next_request_time(),
        )

        return

    followers_data, links = github_api.get_user_followers(user_name, page_link=next_page_link)

    try:
        developer = Developer.objects.get(login=user_name)
    except Developer.DoesNotExist:
        dev_data = github_api.get_user(user_name)
        developer = services.add_or_update_user(dev_data)

    if developer.followers_count == developer.followers.count() and next_page_link is None:
        return

    for follower_data in followers_data:
        dev_data = github_api.get_user(follower_data['login'])
        follower_developer = services.add_or_update_user(dev_data)
        developer.followers.add(follower_developer)

    if 'next' in links.keys():
        add_or_update_user_followers.delay(user_name, links['next'])
