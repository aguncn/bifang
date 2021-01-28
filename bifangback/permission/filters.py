from django_filters import OrderingFilter
from django_filters.rest_framework import FilterSet
from django_filters import filters
from cmdb.models import Permission


class PermissionFilter(FilterSet):
    app = filters.CharFilter(field_name='app__name', lookup_expr='icontains',)
    action = filters.CharFilter(field_name='action__name', lookup_expr='icontains', )
    begin_time = filters.DateTimeFilter(field_name='create_date', lookup_expr='gte',)
    end_time = filters.DateTimeFilter(field_name='create_date', lookup_expr='lte',)
    sort = OrderingFilter(fields=('create_date',))

    class Meta:
        model = Permission
        fields = ['app', 'action', 'begin_time', 'end_time']
