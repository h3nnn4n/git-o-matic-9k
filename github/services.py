from .models import Developer, Repository


def add_or_update_user(data):
    fields = [
        'login',
        'name',
        'location',
        'bio',
        'company',
        'email',

        'created_at',
        'updated_at',

        'followers',
        'following',
        'public_gists',
        'public_repos',
    ]

    defaults = { field: data[field] for field in fields }
    defaults['data_source'] = data

    Developer.objects.update_or_create(
        github_id=data['id'],
        defaults=defaults
    )


def add_or_update_repository(data):
    fields = [
        'name',
        'full_name',
        'description',
        'homepage',
        'language',
        'created_at',
        'updated_at',

        'has_downloads',
        'has_issues',
        'has_pages',
        'has_projects',
        'has_wiki',
        'private',
        'archived',
        'disabled',

        'stargazers_count',
        'subscribers_count',
        'watchers_count',
        'open_issues_count',
    ]

    defaults = { field: data[field] for field in fields }
    defaults['owner_github_id'] = data['owner']['id']
    defaults['data_source'] = data
    defaults['owner'] = Developer.objects.get(github_id=data['owner']['id'])

    Repository.objects.update_or_create(
        github_id=data['id'],
        defaults=defaults
    )