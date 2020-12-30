from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    用户接口
    """
    queryset = User.objects.all().order_by('-date_joined')  # 指定queryset
    serializer_class = UserSerializer  # 指定queryset对应的serializers


class GroupViewSet(viewsets.ModelViewSet):
    """
    用户组接口
    """
    queryset = Group.objects.all()  # 指定queryset
    serializer_class = GroupSerializer  # 指定queryset对应的serializers
