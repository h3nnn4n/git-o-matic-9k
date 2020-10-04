from datetime import datetime, timedelta
from random import randint

import links_from_header
import pytz
import requests

from django.conf import settings

from .models import RateLimit


class HttpErrorExeption(RuntimeError):
    """
    Raised when any error is found. Triggered by a response status code equal
    or greater than 400.
    """


def check_for_errors(response):
    """
    Takes an response and checks if there is any http error. Raises HttpErrorExeption.
    """
    if response.status_code >= 400:
        raise HttpErrorExeption(response.content)


def get_auth():
    """
    Reads the setting file and sets the github api credentials. If not found,
    None is returned and the system runs unauthenticated.
    """
    auth = (settings.GITHUB_API_USER, settings.GITHUB_API_KEY)

    if all(auth):
        return auth

    return None


def rate_limit_update(headers):
    """
    Updates the RateLimit record. triggedred if the remaing api calls count
    decreased or if the reset time increased (this signals a rate limit reset).
    """
    limit = int(headers['X-RateLimit-Limit'])
    remaining = int(headers['X-RateLimit-Remaining'])
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


def next_request_time():
    """
    Returns when the next request can be made, based on the rate api data from
    github's api. A fudge factor of 1~60 seconds is added to prevent the system
    from being bombarded with too many tasks at once.
    """
    ratelimit = RateLimit.objects.get(pk=1)
    return ratelimit.rate_reset + timedelta(seconds=randint(1, 60))


def can_make_new_requests():
    """
    Check if it is possible to make new requests. This compares the RateLimit
    remaining data agaisnt the RATE_LIMIT_STOP_THRESHOLD setting
    """
    try:
        ratelimit = RateLimit.objects.get(pk=1)
        return ratelimit.can_make_new_requests()
    except RateLimit.DoesNotExist:
        return True


def get_user(user_name):
    """
    Fetches a github developer (user). Receives an username/login. E.g.
    'h3nnn4n'
    """
    auth = get_auth()

    result = requests.get(
        f'https://api.github.com/users/{user_name}',
        auth=auth
    )

    rate_limit_update(result.headers)
    check_for_errors(result)

    return result.json()


def get_repository(repo_name):
    """
    Fetches a github repository. Receives a repository full name. E.g.
    'h3nnn4n/garapa'
    """
    auth = get_auth()

    result = requests.get(
        f'https://api.github.com/repos/{repo_name}',
        auth=auth
    )

    rate_limit_update(result.headers)
    check_for_errors(result)

    return result.json()


def list_repositories(user_name, page_link=None):
    """
    Lists a developer's repositories. Receives an username/login. E.g.
    'h3nnn4n'. This is paginated. The first query returns a 'next' link, which
    should be passed back to this function via the `page_link` parameter.
    """
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


def get_user_followers(user_name, page_link=None):
    """
    Lists a developer's followers list. Receives an username/login. E.g.
    'h3nnn4n'. This is paginated. The first query returns a 'next' link, which
    should be passed back to this function via the `page_link` parameter.
    """
    auth = get_auth()

    result = requests.get(
        page_link or f'https://api.github.com/users/{user_name}/followers',
        auth=auth
    )

    rate_limit_update(result.headers)
    check_for_errors(result)

    if 'link' in result.headers.keys():
        links = links_from_header.extract(result.headers['link'])
    else:
        links = {}

    return result.json(), links


def get_user_followings(user_name, page_link=None):
    """
    Lists a developer's following list. Receives an username/login. E.g.
    'h3nnn4n'. This is paginated. The first query returns a 'next' link, which
    should be passed back to this function via the `page_link` parameter.
    """
    auth = get_auth()

    result = requests.get(
        page_link or f'https://api.github.com/users/{user_name}/following',
        auth=auth
    )

    rate_limit_update(result.headers)
    check_for_errors(result)

    if 'link' in result.headers.keys():
        links = links_from_header.extract(result.headers['link'])
    else:
        links = {}

    return result.json(), links


def get_user_stared_repositories(user_name, page_link=None):
    """
    Lists a developer's starred repositories. Receives an username/login. E.g.
    'h3nnn4n'. This is paginated. The first query returns a 'next' link, which
    should be passed back to this function via the `page_link` parameter.
    """
    auth = get_auth()

    result = requests.get(
        page_link or f'https://api.github.com/users/{user_name}/starred',
        auth=auth
    )

    rate_limit_update(result.headers)
    check_for_errors(result)

    if 'link' in result.headers.keys():
        links = links_from_header.extract(result.headers['link'])
    else:
        links = {}

    return result.json(), links


def get_repository_stargazers(repo_name, page_link=None):
    """
    Lists a repository stargazers. Receives a repository full name. E.g.
    'h3nnn4n/garapa'. This is paginated. The first query returns a 'next' link,
    which should be passed back to this function via the `page_link` parameter.
    """
    auth = get_auth()

    result = requests.get(
        page_link or f'https://api.github.com/repos/{repo_name}/stargazers',
        auth=auth
    )

    rate_limit_update(result.headers)
    check_for_errors(result)

    if 'link' in result.headers.keys():
        links = links_from_header.extract(result.headers['link'])
    else:
        links = {}

    return result.json(), links
