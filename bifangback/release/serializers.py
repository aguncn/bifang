from abc import ABC

from rest_framework import serializers
from cmdb.models import Release


class ReleaseSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='app.project.name', default="None")
    app_name = serializers.CharField(source='app.name', default="None")
    service_port = serializers.CharField(source='app.service_port', default="None")
    env_name = serializers.CharField(source='env.name', default="None")
    create_user_name = serializers.CharField(source='create_user.username')
    release_status_name = serializers.CharField(source='release_status.name', default="None")
    git_url = serializers.CharField(source='app.git.git_url', default="None")
    git_app_id = serializers.CharField(source='app.git_app_id', default="None")

    class Meta:
        model = Release
        fields = '__all__'

class ReleaseStatisticsSerializer(serializers.ModelSerializer):
    app_name = serializers.CharField(source='app.name', default="None")
    release_count = serializers.CharField()
    class Meta:
        model = Release
        fields = ['app_id','app_name','release_count']

class ReleaseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Release
        # fields = '__all__'
        fields = ['name', 'description', 'git_branch', 'app', 'release_status', 'create_user']


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

