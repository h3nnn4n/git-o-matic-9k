import requests
import links_from_header

from django.conf import settings


class HttpErrorExeption(RuntimeError):
    pass


def check_for_errors(response):
    if response.status_code >= 400:
        raise HttpErrorExeption(response.content)


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

    check_for_errors(result)

    return result.json()


def get_repository(repo_name):
    auth = get_auth()

    result = requests.get(
        f'https://api.github.com/repos/{repo_name}',
        auth=auth
    )

    check_for_errors(result)

    return result.json()


def list_repositories(user_name, page_link=None):
    auth = get_auth()

    result = requests.get(
        page_link or f'https://api.github.com/users/{user_name}/repos',
        auth=auth
    )

    check_for_errors(result)

    links = links_from_header.extract(result.headers['link'])

    return result.json(), links
