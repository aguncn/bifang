from rest_framework import serializers
from cmdb.models import App


class AppSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', default="None")
    git_name = serializers.CharField(source='git.name', default="None")

    class Meta:
        model = App
        fields = '__all__'
