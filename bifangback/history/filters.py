from django_filters import OrderingFilter
from django_filters.rest_framework import FilterSet
from django_filters import filters
from cmdb.models import ReleaseHistory
from cmdb.models import ServerHistory


class ReleaseHistoryFilter(FilterSet):
    release = filters.CharFilter(field_name='release__name', lookup_expr='icontains',)
    begin_time = filters.DateTimeFilter(field_name='create_date', lookup_expr='gte',)
    end_time = filters.DateTimeFilter(field_name='create_date', lookup_expr='lte',)
    sort = OrderingFilter(fields=('create_date',))

    class Meta:
        model = ReleaseHistory
        fields = ['release_id', 'begin_time', 'end_time']


class ServerHistoryFilter(FilterSet):
    server = filters.CharFilter(field_name='server__name', lookup_expr='icontains',)
    begin_time = filters.DateTimeFilter(field_name='create_date', lookup_expr='gte',)
    end_time = filters.DateTimeFilter(field_name='create_date', lookup_expr='lte',)
    sort = OrderingFilter(fields=('create_date',))

    class Meta:
        model = ServerHistory
        fields = ['server', 'begin_time', 'end_time']
