from django_filters import OrderingFilter
from django_filters.rest_framework import FilterSet
from django_filters import filters
from cmdb.models import Env


class EnvFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains',)
    begin_time = filters.DateTimeFilter(field_name='create_date', lookup_expr='gte',)
    end_time = filters.DateTimeFilter(field_name='create_date', lookup_expr='lte',)
    sort = OrderingFilter(fields=('create_date',))
    project_name = filters.CharFilter(field_name='project_name', method='project_name_filter')
    app_name = filters.CharFilter(field_name='app_name', method='app_name_filter')

    def project_name_filter(self, queryset, field_name, value):
        # 外建基于列表过滤的语法
        return queryset.filter(app__project__name__exact=value)

    def app_name_filter(self, queryset, field_name, value):
        # 外建基于列表过滤的语法
        return queryset.filter(app__name__exact=value)

    class Meta:
        model = Env
        fields = ['name', 'project_name', 'app_name', 'begin_time', 'end_time']
