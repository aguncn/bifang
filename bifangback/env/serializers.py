from rest_framework import serializers
from cmdb.models import Env


class EnvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Env
        fields = '__all__'


class EnvExchangeSerializer(serializers.Serializer):
    release_name = serializers.CharField(max_length=100)
    env_id = serializers.CharField(max_length=64)
    app_id = serializers.CharField(max_length=64)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

