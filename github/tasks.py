from celery import shared_task

from . import github_api


@shared_task
def get_user(user_name):
    result = github_api.get_user(user_name)
    print(result)
    return result
