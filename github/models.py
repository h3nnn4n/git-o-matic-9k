import uuid
from django.db import models
from django.db.models import JSONField
from django.conf import settings


class Developer(models.Model):
    """
    Represents a github user
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    github_id = models.CharField(max_length=256)
    # It appears that github limits the length to 39, but lets keep it long
    # enough to be future proof
    login = models.CharField(max_length=256)
    name = models.TextField(null=True)
    location = models.TextField(null=True)
    bio = models.TextField(null=True)
    company = models.TextField(null=True)
    email = models.TextField(null=True)

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    followers = models.ManyToManyField('Developer', related_name='reverse_followers')
    following = models.ManyToManyField('Developer', related_name='reverse_following')

    starred_repositories = models.ManyToManyField('Repository', related_name='reverse_starred')

    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    public_gists = models.IntegerField(default=0)
    public_repos = models.IntegerField(default=0)

    data_source = JSONField()

    def missing_followers(self):
        """
        Return True if the number of reported followers by github differs from
        the number of followers in the database. Returns False, otherwise.
        Useful for detecting out of sync data.
        """
        return self.followers_count != self.followers.count()

    def missing_following(self):
        """
        Return True if the number of reported following users by github differs
        from the number of following users in the database. Returns False,
        otherwise.  Useful for detecting out of sync data.
        """
        return self.following_count != self.following.count()

    def missing_repositories(self):
        """
        Return True if the number of reported repositories by github differs
        from the number of repositories in the database. Returns False,
        otherwise.  Useful for detecting out of sync data.
        """
        return self.public_repos != self.repositories.count()


class Repository(models.Model):
    """
    Represents a github repository
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='repositories')
    github_id = models.CharField(max_length=256)
    owner_github_id = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    full_name = models.CharField(max_length=256)
    description = models.TextField(null=True)
    homepage = models.TextField(null=True)
    language = models.TextField(null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    has_downloads = models.BooleanField()
    has_issues = models.BooleanField()
    has_pages = models.BooleanField()
    has_projects = models.BooleanField()
    has_wiki = models.BooleanField()
    private = models.BooleanField()
    archived = models.BooleanField()
    disabled = models.BooleanField()

    stargazers = models.ManyToManyField('Developer', related_name='reverse_stargazers')

    stargazers_count = models.IntegerField()
    subscribers_count = models.IntegerField()
    watchers_count = models.IntegerField()
    open_issues_count = models.IntegerField()

    data_source = JSONField()


class RateLimit(models.Model):
    """
    Represents the rate limit data from github. Used for throtting
    """
    rate_limit = models.IntegerField()
    rate_remaining = models.IntegerField()
    rate_reset_raw = models.IntegerField()
    rate_reset = models.DateTimeField()

    def can_make_new_requests(self):
        """
        Return True if there are enough remaining requests in the quota to make
        a new request.
        """
        return self.rate_remaining > settings.RATE_LIMIT_STOP_THRESHOLD
