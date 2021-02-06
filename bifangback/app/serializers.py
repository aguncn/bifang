from rest_framework import serializers
from cmdb.models import App


class AppSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name')

    class Meta:
        model = App
        fields = '__all__'
