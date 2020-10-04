from celery import shared_task

from . import services
from . import github_api

from .models import Developer, Repository


@shared_task
def discovery_scraper(count=5):
    """
    Finds up to five users where some of the data is out of date or missing.
    The number of users to be updated can be changed with the `count`
    parameter. An user is selected if the number of records reported by github
    differs from the count in the database for any of the following
    fields/relations: followers, following, repositories. This triggers the
    `full_profile_sync` task.
    """
    enqueued = 0

    for developer in Developer.objects.all():
        trigger_conditions = [
            developer.missing_followers(),
            developer.missing_following(),
            developer.missing_repositories(),
        ]

        if any(trigger_conditions):
            full_profile_sync.delay(developer.login)
            enqueued += 1

        if enqueued >= count:
            break


@shared_task
def full_profile_sync(user_name):
    """
    Sync all data for a given username/login. This service is very granular and
    it spawns several other tasks.
    """
    add_or_update_user.delay(user_name)
    add_or_update_all_user_repositories.delay(user_name, populate_stargazers=True)
    add_or_update_user_followers.delay(user_name)
    add_or_update_user_followings.delay(user_name)
    add_or_update_user_starred_repositories.delay(user_name)


@shared_task
def add_or_update_user(user_name):
    """
    Adds or update an user specified by its username/login.
    """
    if not github_api.can_make_new_requests():
        add_or_update_user.apply_async(
            args=[user_name],
            eta=github_api.next_request_time(),
        )

        return

    dev_data = github_api.get_user(user_name)

    services.add_or_update_user(dev_data)


@shared_task
def add_or_update_repository(repo_name, populate_stargazers=False):
    """
    Adds or update a repository specified by its full name. E.g.
    'h3nnn4n/garapa'. If the owner user doesnt exist, it is created too.
    The optional parameter `populate_stargazers` triggers populating
    the stargazers relation with the respective users. This can be very time
    consuming for some popular repositories and can easily take hours to sync.
    """
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

    if populate_stargazers:
        add_or_update_repository_stargazers(repo_name)


@shared_task
def add_or_update_all_user_repositories(user_name, next_page_link=None, populate_stargazers=False):
    """
    Syncs all repositories for an user. If the owner user doesnt exist, it is
    created too.  The optional parameter `populate_stargazers` triggers
    populating the stargazers relation with the respective users. This can be
    very time consuming for some popular repositories and can easily take hours
    to sync.
    """
    if not github_api.can_make_new_requests():
        add_or_update_all_user_repositories.apply_async(
            args=[user_name, next_page_link],
            eta=github_api.next_request_time(),
        )

        return

    all_repo_data, links = github_api.list_repositories(user_name, page_link=next_page_link)

    for repo_data in all_repo_data:
        add_or_update_repository.delay(repo_data['full_name'], populate_stargazers=populate_stargazers)

    if 'next' in links.keys():
        add_or_update_all_user_repositories(user_name, links['next'])


@shared_task
def add_or_update_user_followers(user_name, next_page_link=None):
    """
    Fetches, updates and creates all followers of a given user. If the user
    itself doesnt exist it is created. The task returns without changing any
    data if the followers count on disk matches the last count from github.
    """
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
        follower_developer.following.add(developer)

    if 'next' in links.keys():
        add_or_update_user_followers.delay(user_name, links['next'])


@shared_task
def add_or_update_user_followings(user_name, next_page_link=None):
    """
    Fetches, updates and creates all following users of a given user. If the
    user itself doesnt exist it is created. The task returns without changing
    any data if the following count on disk matches the last count from github.
    """
    if not github_api.can_make_new_requests():
        add_or_update_user_followings.apply_async(
            args=[user_name, next_page_link],
            eta=github_api.next_request_time(),
        )

        return

    followeds_data, links = github_api.get_user_followings(user_name, page_link=next_page_link)

    try:
        developer = Developer.objects.get(login=user_name)
    except Developer.DoesNotExist:
        dev_data = github_api.get_user(user_name)
        developer = services.add_or_update_user(dev_data)

    if developer.following_count == developer.following.count() and next_page_link is None:
        return

    for followed_data in followeds_data:
        dev_data = github_api.get_user(followed_data['login'])
        followed_developer = services.add_or_update_user(dev_data)
        developer.following.add(followed_developer)
        followed_developer.followers.add(developer)

    if 'next' in links.keys():
        add_or_update_user_followings.delay(user_name, links['next'])


@shared_task
def add_or_update_user_starred_repositories(user_name, next_page_link=None):
    """
    Fetches, updates and creates all repositories starred by a given user. If
    the user itself doesnt exist it is created. The repository owner users are
    also created if they doesnt exist. If they do, they get updated. The task
    returns without changing any data if the repository count on disk matches
    the last count from github.
    """
    if not github_api.can_make_new_requests():
        add_or_update_user_starred_repositories.apply_async(
            args=[user_name, next_page_link],
            eta=github_api.next_request_time(),
        )

        return

    starred_repositories, links = github_api.get_user_stared_repositories(user_name, page_link=next_page_link)

    try:
        developer = Developer.objects.get(login=user_name)
    except Developer.DoesNotExist:
        dev_data = github_api.get_user(user_name)
        developer = services.add_or_update_user(dev_data)

    for starred_repository_data in starred_repositories:
        repo_data = github_api.get_repository(starred_repository_data['full_name'])
        add_or_update_user(repo_data['owner']['login'])
        starred_repository = services.add_or_update_repository(repo_data)
        developer.starred_repositories.add(starred_repository)
        starred_repository.stargazers.add(developer)

    if 'next' in links.keys():
        add_or_update_user_starred_repositories.delay(user_name, links['next'])


@shared_task
def add_or_update_repository_stargazers(repo_name, next_page_link=None):
    """
    Fetches, updates and creates all stargazer users for a given repository. If
    the repository itself doesnt exist it is created. Same for the owner user.
    The task returns without changing any data if the stargazer count on disk
    matches the last count from github.
    """
    if not github_api.can_make_new_requests():
        add_or_update_repository_stargazers.apply_async(
            args=[repo_name, next_page_link],
            eta=github_api.next_request_time(),
        )

        return

    stargazers_data, links = github_api.get_repository_stargazers(repo_name, page_link=next_page_link)

    try:
        repository = Repository.objects.get(full_name=repo_name)
    except Developer.DoesNotExist:
        repo_data = github_api.get_repository(repo_name)
        repository = services.add_or_update_repository(repo_data)

    if repository.stargazers_count == repository.stargazers.count() and next_page_link is None:
        return

    assert repository is not None

    for stargazer_data in stargazers_data:
        user_data = github_api.get_user(stargazer_data['login'])
        stargazer = services.add_or_update_user(user_data)

        repository.stargazers.add(stargazer)
        stargazer.starred_repositories.add(repository)

    if 'next' in links.keys():
        add_or_update_repository_stargazers.delay(repo_name, links['next'])
