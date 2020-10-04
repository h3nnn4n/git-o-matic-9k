class Task():
    """
    A simple set of hardcoded actions
    """
    def __init__(self, **kwargs):
        for field in ('id', 'name', 'username', 'repo_name'):
            setattr(self, field, kwargs.get(field, None))

TASKS = {
    1: Task(id=1, name='full_profile_sync', username='required', repo_name='n/a'),
    2: Task(id=2, name='full_repository_sync', username='required', repo_name='required'),
    3: Task(id=3, name='discovery_scraper', username='n/a', repo_name='n/a'),
}
