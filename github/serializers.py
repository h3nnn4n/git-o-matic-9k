from rest_framework import serializers

from .models import Developer, Repository


class DeveloperSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Developer
        exclude = ['data_source']


class RepositorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Repository
        exclude = ['data_source']
