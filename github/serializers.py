from rest_framework import serializers

from .models import Developer, Repository, RateLimit


class RepositorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
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
    class Meta:
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
    class Meta:
        model = RateLimit
        fields = '__all__'
