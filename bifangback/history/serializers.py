from rest_framework import serializers
from cmdb.models import ReleaseHistory
from cmdb.models import ServerHistory


class ReleaseHistorySerializer(serializers.ModelSerializer):
    env = serializers.CharField(source='env.name', default=None)
    release = serializers.CharField(source='release.name', default=None)
    create_user = serializers.CharField(source='create_user.username', default=None)
    release_status_name = serializers.CharField(source='release_status.name', default=None)

    class Meta:
        model = ReleaseHistory
        fields = '__all__'


class ServerHistorySerializer(serializers.ModelSerializer):
    server = serializers.CharField(source='server.name', default=None)
    env = serializers.CharField(source='env.name', default=None)
    release = serializers.CharField(source='release.name', default=None)
    create_user = serializers.CharField(source='create_user.username')

    class Meta:
        model = ServerHistory
        fields = '__all__'

