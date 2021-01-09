from django_filters import OrderingFilter
from django_filters.rest_framework import FilterSet
from django_filters import filters
from cmdb.models import Env


class EnvFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains',)
    begin_time = filters.DateTimeFilter(field_name='create_date', lookup_expr='gte',)
    end_time = filters.DateTimeFilter(field_name='create_date', lookup_expr='lte',)
    sort = OrderingFilter(fields=('create_date',))

    class Meta:
        model = Env
        fields = ['name', 'begin_time', 'end_time']