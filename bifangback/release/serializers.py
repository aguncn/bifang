from abc import ABC

from rest_framework import serializers
from cmdb.models import Release


class ReleaseSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='app.project.name')
    app_name = serializers.CharField(source='app.name')
    env_name = serializers.CharField(source='env.name', default="None")
    create_user_name = serializers.CharField(source='create_user.username')
    deploy_status_name = serializers.CharField(source='deploy_status.name')
    git_url = serializers.CharField(source='app.git.git_url')
    git_app_id = serializers.CharField(source='app.git_app_id')

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

