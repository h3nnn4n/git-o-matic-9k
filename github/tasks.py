from celery import shared_task

from .models import Developer
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
