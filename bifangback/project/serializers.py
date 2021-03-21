from rest_framework import serializers
from cmdb.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    create_user_name = serializers.CharField(source='create_user.username')
    class Meta:
        model = Project
        fields = '__all__'
