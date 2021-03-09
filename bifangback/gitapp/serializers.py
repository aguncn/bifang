from rest_framework import serializers
from cmdb.models import GitTb


class GitappSerializer(serializers.ModelSerializer):
    class Meta:
        model = GitTb
        fields = ['id', 'name']
