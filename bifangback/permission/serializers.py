from rest_framework import serializers
from cmdb.models import Permission


class PermissionSerializer(serializers.ModelSerializer):
    app = serializers.CharField(source='app.name')
    action = serializers.CharField(source='action.name')
    create_user = serializers.CharField(source='create_user.username')
    pm_user = serializers.CharField(source='pm_user.username')

    class Meta:
        model = Permission
        fields = '__all__'
