from rest_framework import serializers
from cmdb.models import Permission


class PermissionSerializer(serializers.ModelSerializer):
    app_name = serializers.CharField(source='app.name', read_only=True)
    action_name = serializers.CharField(source='action.name', read_only=True)
    create_username = serializers.CharField(source='create_user.username', read_only=True)
    pm_username = serializers.CharField(source='pm_user.username', read_only=True)

    class Meta:
        model = Permission
        fields = '__all__'
