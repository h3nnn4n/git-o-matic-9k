from datetime import datetime

import links_from_header
import pytz
import requests

from django.conf import settings

from .models import RateLimit


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


def rate_limit_update(headers):
    limit = headers['X-RateLimit-Limit']
    remaining = headers['X-RateLimit-Remaining']
    reset = int(headers['X-RateLimit-Reset'])
    reset_datetime = datetime.utcfromtimestamp(reset)
    reset_datetime = pytz.utc.localize(reset_datetime)

    obj, created = RateLimit.objects.update_or_create(
        id=1,
        defaults={
            'rate_limit': limit,
            'rate_remaining': remaining,
            'rate_reset': reset_datetime,
            'rate_reset_raw': reset,
        }
    )

    if created:
        return

    if reset > obj.rate_reset_raw or obj.rate_remaining > remaining:
        obj.rate_reset_raw = reset
        obj.rate_reset = reset_datetime
        obj.rate_limit = limit
        obj.rate_remaining = remaining


def get_user(user_name):
    auth = get_auth()

    result = requests.get(
        f'https://api.github.com/users/{user_name}',
        auth=auth
    )

    rate_limit_update(result.headers)
    check_for_errors(result)

    return result.json()


def get_repository(repo_name):
    auth = get_auth()

    result = requests.get(
        f'https://api.github.com/repos/{repo_name}',
        auth=auth
    )

    rate_limit_update(result.headers)
    check_for_errors(result)

    return result.json()


def list_repositories(user_name, page_link=None):
    auth = get_auth()

    result = requests.get(
        page_link or f'https://api.github.com/users/{user_name}/repos',
        auth=auth
    )

    rate_limit_update(result.headers)
    check_for_errors(result)

    if 'link' in result.headers.keys():
        links = links_from_header.extract(result.headers['link'])
    else:
        links = {}

    return result.json(), links
