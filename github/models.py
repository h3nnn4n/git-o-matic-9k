import uuid
from django.db import models
from django.db.models import JSONField


class Developer(models.Model):
    """
        Represents a github user
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    github_id = models.CharField(max_length=256)
    # It appears that github limits the length to 39, but lets keep it long
    # enough to be future proof
    user_name = models.CharField(max_length=256)
    data_source = JSONField()


class Repository(models.Model):
    """
        Represents a github repository
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    description = models.TextField()
    github_id = models.CharField(max_length=256)
    data_source = JSONField()
