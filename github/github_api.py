import requests

from django.conf import settings


def get_user(user_name):
    auth = (settings.GITHUB_API_USER, settings.GITHUB_API_KEY)

    if auth[0] is not None:
        return requests.get(
            f'https://api.github.com/users/{user_name}',
            auth=auth
        )

    return requests.get(
        f'https://api.github.com/users/{user_name}',
    )
