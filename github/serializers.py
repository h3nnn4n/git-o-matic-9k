from rest_framework import serializers

from .models import Developer, Repository, RateLimit
from .enumerations import Task


class RepositorySerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for a Repository
    """
    class Meta: # pylint: disable=missing-class-docstring
        model = Repository
        fields = [
            'owner',
            'github_id',
            'owner_github_id',
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

            'stargazers',

            'stargazers_count',
            'subscribers_count',
            'watchers_count',
            'open_issues_count',
        ]


class DeveloperSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for a Developer
    """
    class Meta: # pylint: disable=missing-class-docstring
        model = Developer
        fields = [
            'github_id',
            'login',
            'name',
            'location',
            'bio',
            'company',
            'email',
            'created_at',
            'updated_at',
            'followers_count',
            'following_count',
            'public_gists',
            'public_repos',
            'followers',
            'following',
            'starred_repositories',
            'repositories',
        ]


class RateLimitSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for the RateLimit record
    """
    class Meta: # pylint: disable=missing-class-docstring
        model = RateLimit
        fields = '__all__'


class TaskSerializer(serializers.Serializer):
    """
    Serializer that exposes app tasks. I.e. endpoint that trigger an action
    """
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=256, read_only=False)
    username = serializers.CharField(max_length=256, read_only=False)
    repo_name = serializers.CharField(max_length=256, read_only=False)

    def create(self, validated_data):
        return Task(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance
