from rest_framework import serializers
from cmdb.models import ReleaseHistory


class ReleaseHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReleaseHistory
        fields = '__all__'
