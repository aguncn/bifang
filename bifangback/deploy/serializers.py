from rest_framework import serializers
from cmdb.models import Release


class ReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Release
        fields = '__all__'


class DeploySerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=16)
    app_name = serializers.CharField(max_length=100)
    release_name = serializers.CharField(max_length=64)
    env_name = serializers.CharField(max_length=16)
    deploy_type = serializers.CharField(max_length=64)
    op_type = serializers.CharField(max_length=64)
    target_list = serializers.ListField(required=True, child=serializers.CharField(),)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
