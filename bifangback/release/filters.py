from django.db.models import Q
from django_filters import OrderingFilter
from django_filters.rest_framework import FilterSet
from django_filters import filters
from cmdb.models import Release


class ReleaseFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains',)
    begin_time = filters.DateTimeFilter(field_name='create_date', lookup_expr='gte',)
    end_time = filters.DateTimeFilter(field_name='create_date', lookup_expr='lte',)
    sort = OrderingFilter(fields=('create_date',))
    # 自定义过滤方法
    deploy_status = filters.CharFilter(field_name='deploy_status', method='deploy_status_filter', )

    def deploy_status_filter(self, queryset, field_name, value):
        # 前端传过来的deploy_status为字符串，将其转换为列表，就可以过滤需要的发布单了
        filter_list = value.split(',')
        # 外建基于列表过滤的语法
        return queryset.filter(deploy_status__name__in=filter_list)

    class Meta:
        model = Release
        fields = ['name', 'begin_time', 'end_time', 'deploy_status']
