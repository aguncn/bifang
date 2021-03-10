from rest_framework import serializers
from cmdb.models import Server


class ServerSerializer(serializers.ModelSerializer):
    app_name = serializers.CharField(source='app.name', default="None", read_only=True)
    project_name = serializers.CharField(source='app.project.name', default="None", read_only=True)
    env_name = serializers.CharField(source='env.name', default="None", read_only=True)
    main_release_name = serializers.CharField(source='main_release.name', default="None", required=False, read_only=True)
    back_release_name = serializers.CharField(source='back_release.name', default="None", required=False, read_only=True)
    create_username = serializers.CharField(source='create_user.username', default="None", read_only=True)

    class Meta:
        model = Server
        fields = '__all__'
