from django_filters import OrderingFilter
from django_filters.rest_framework import FilterSet
from django_filters import filters
from cmdb.models import Server


class ServerFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains',)
    begin_time = filters.DateTimeFilter(field_name='create_date', lookup_expr='gte',)
    end_time = filters.DateTimeFilter(field_name='create_date', lookup_expr='lte',)
    sort = OrderingFilter(fields=('create_date',))

    class Meta:
        model = Server
        fields = ['name', 'app_id', 'env_id', 'begin_time', 'end_time']
