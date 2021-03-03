from rest_framework import serializers
from cmdb.models import Server


class ServerSerializer(serializers.ModelSerializer):
    app_name = serializers.CharField(source='app.name', default=None)
    project_name = serializers.CharField(source='app.project.name', default=None)
    env_name = serializers.CharField(source='env.name',  default=None)
    create_username = serializers.CharField(source='create_user.username', default=None)

    class Meta:
        model = Server
        fields = '__all__'
