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
    release_name = filters.CharFilter(field_name='release__name', lookup_expr='icontains',)
    env_name = filters.CharFilter(field_name='env__name', lookup_expr='icontains', )
    begin_time = filters.DateTimeFilter(field_name='create_date', lookup_expr='gte',)
    end_time = filters.DateTimeFilter(field_name='create_date', lookup_expr='lte',)
    sort = OrderingFilter(fields=('create_date',))

    class Meta:
        model = ServerHistory
        fields = ['release_name', 'env_name', 'release_id', 'env_id', 'log_no', 'begin_time', 'end_time']
