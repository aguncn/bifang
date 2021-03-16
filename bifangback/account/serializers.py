from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class GroupsReadOnly(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    # many-to-many的字段序列化
    groups_names = GroupsReadOnly(source='groups', many=True, read_only=True)

    class Meta:
        model = User  # 要序列的model
        fields = ('id', 'url', 'username', 'email', 'groups', 'groups_names')  # 数据字段


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group  # 要序列的model
        fields = ('url', 'name', 'id')  # 数据字段
