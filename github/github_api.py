import requests

from django.conf import settings
from django.utils.dateparse import parse_datetime


def get_auth():
    auth = (settings.GITHUB_API_USER, settings.GITHUB_API_KEY)

    if all(auth):
        return auth

    return None


def get_user(user_name):
    auth = get_auth()

    result = requests.get(
        f'https://api.github.com/users/{user_name}',
        auth=auth
    )

    return result.json()


def get_repository(repo_name):
    auth = get_auth()

    result = requests.get(
        f'https://api.github.com/repos/{repo_name}',
        auth=auth
    )

    return result.json()


def list_repositories(user_name):
    auth = get_auth()

    result = requests.get(
        f'https://api.github.com/users/{user_name}/repos',
        auth=auth
    )

    return result.json()
