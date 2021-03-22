from django.db.models import F
from django.db.models import Count
from cmdb.models import Project
from cmdb.models import App
from cmdb.models import Release
from cmdb.models import ReleaseStatus
from utils.ret_code import *


# 输出项目，组件，发布单总数
def all_count(request):
    project_count = Project.objects.count()
    app_count = App.objects.count()
    release_count = Release.objects.count()
    data = {
        'project': project_count,
        'app': app_count,
        'release': release_count
    }
    return_dict = build_ret_data(OP_SUCCESS, data)
    return render_json(return_dict)


# 输出各组件发布单总量top5
def release_top5(request):
    queryset = Release.objects.values('app_id') \
                   .annotate(release_count=Count('name'), app_name=F('app__name')) \
                   .order_by('-release_count')[:5]
    data = {'app_name': [],
            'release_count': []}
    for item in queryset:
        data['app_name'].append(item['app_name'])
        data['release_count'].append(item['release_count'])
    print(data)
    return_dict = build_ret_data(OP_SUCCESS, data)
    return render_json(return_dict)


# 输出各组件发布单错误数量top5
def release_failed_top5(request):
    deploy_status = ReleaseStatus.objects.get(name='Failed')
    queryset = Release.objects.filter(deploy_status=deploy_status).values('app_id') \
                   .annotate(release_count=Count('name'), app_name=F('app__name')) \
                   .order_by('-release_count')[:5]
    data = {'app_name': [],
            'release_count': []}
    for item in queryset:
        data['app_name'].append(item['app_name'])
        data['release_count'].append(item['release_count'])
    print(data)
    return_dict = build_ret_data(OP_SUCCESS, data)
    return render_json(return_dict)
