from django.db.models import Q
from django_filters import OrderingFilter
from django_filters.rest_framework import FilterSet
from django_filters import filters
from cmdb.models import Release


class ReleaseFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains',)
    begin_time = filters.DateTimeFilter(field_name='create_date', lookup_expr='gte',)
    end_time = filters.DateTimeFilter(field_name='create_date', lookup_expr='lte',)
    sort = OrderingFilter(fields=('create_date','update_date'))
    # 自定义过滤方法
    release_status = filters.CharFilter(field_name='release_status', method='release_status_filter')
    project_name = filters.CharFilter(field_name='project_name', method='project_name_filter')
    app_name = filters.CharFilter(field_name='app_name', method='app_name_filter')

    def release_status_filter(self, queryset, field_name, value):
        # 前端传过来的deploy_status为字符串，将其转换为列表，就可以过滤需要的发布单了
        filter_list = value.split(',')
        # 外建基于列表过滤的语法
        return queryset.filter(release_status__name__in=filter_list)
    
    def project_name_filter(self, queryset, field_name, value):
        # 外建基于列表过滤的语法
        return queryset.filter(app__project__name__exact=value)

    def app_name_filter(self, queryset, field_name, value):
        # 外建基于列表过滤的语法
        return queryset.filter(app__name__exact=value)

    class Meta:
        model = Release
        fields = ['name', 'project_name', 'app_name', 'begin_time', 'end_time', 'release_status']
