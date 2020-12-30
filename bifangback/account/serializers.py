from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # 要序列的model
        fields = ('url', 'username', 'email', 'groups')  # 数据字段


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group  # 要序列的model
        fields = ('url', 'name')  # 数据字段
