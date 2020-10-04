from rest_framework import serializers

from .models import Developer, Repository, RateLimit


class RepositorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Repository
        exclude = ['data_source']


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
            'repositories',
        ]


class RateLimitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RateLimit
        fields = '__all__'
