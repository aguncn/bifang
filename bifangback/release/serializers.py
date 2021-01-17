from abc import ABC

from rest_framework import serializers
from cmdb.models import Release


class ReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Release
        fields = '__all__'


class ReleaseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Release
        # fields = '__all__'
        fields = ['name', 'description', 'git_branch', 'app', 'deploy_status', 'create_user']


class ReleaseBuildSerializer(serializers.Serializer):
    app_name = serializers.CharField(max_length=100)
    release_name = serializers.CharField(max_length=64)
    git_branch = serializers.CharField(max_length=64)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ReleaseBuildStatusSerializer(serializers.Serializer):
    app_name = serializers.CharField(max_length=100)
    release_name = serializers.CharField(max_length=64)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

