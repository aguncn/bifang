from django.conf import settings
from cmdb.models import App
from utils.gitlab import gitlab_trigger
from utils.gitlab import pipeline_status
from cmdb.models import Release
from cmdb.models import ReleaseStatus
from .serializers import ReleaseSerializer
from .serializers import ReleaseBuildSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from utils.ret_code import *
from .filters import ReleaseFilter


class ReleaseListView(ListAPIView):
    queryset = Release.objects.all()
    serializer_class = ReleaseSerializer
    filter_class = ReleaseFilter

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)


class ReleaseBuildView(APIView):
    """
    编译软件

    参数:
    app_name
    release_name
    git_branch
    """
    def post(self, request):
        req_data = request.data
        ser_data = ReleaseBuildSerializer(req_data)
        if ser_data.is_valid():
            app_name = ser_data['app_name']
            app = App.objects.get(name=app_name)
            git_url = app.git.git_url
            git_access_token = app.git.git_token
            git_trigger_token = app.git_trigger_token
            project_id = app.git_app_id
            release = ser_data['release_name']
            git_branch = ser_data['git_branch']
            build_script = app.build_script
            deploy_script = app.deploy_script
            file_up_server = settings.FILE_UP_SERVER
            # 先触发编译，但由于编译时间较长，为防连接过期，异步一下，先返回id，再获取编译状态
            pipeline = gitlab_trigger(git_url, git_access_token,
                                      project_id, app_name, release,
                                      git_branch, git_trigger_token,
                                      build_script, deploy_script, file_up_server)
            # 在编译前，更新一下发布单的状态，待写编译历史库记录
            deploy_status = ReleaseStatus.objects.get(name='Building')
            Release.objects.filter(name=release).update(pipeline_id=pipeline.id,
                                                        pipeline_url=pipeline.web_url,
                                                        deploy_status=deploy_status)

            return_dict = build_ret_data(OP_SUCCESS, pipeline.id)
            return render_json(return_dict)
        else:
            return_dict = build_ret_data(THROW_EXP, '序列化条件不满足')
            return render_json(return_dict)


class ReleaseBuildStatusView(APIView):
    """
    获取编译软件状态

    参数:
    app_name
    release_name
    """
    def post(self, request):
        req_data = request.data
        ser_data = ReleaseBuildSerializer(req_data)
        if ser_data.is_valid():
            app_name = ser_data['app_name']
            app = App.objects.get(name=app_name)
            git_url = app.git.git_url
            git_access_token = app.git.git_token
            project_id = app.git_app_id
            release = Release.objects.get(name=ser_data['release_name'])
            pipeline_id = release.pipeline_id

            pipeline = pipeline_status(git_url, git_access_token, project_id, pipeline_id)
            if pipeline.finished_at is None:
                return_dict = build_ret_data(OP_SUCCESS, 'ing')
                return render_json(return_dict)
            elif pipeline.status != 'success':
                return_dict = build_ret_data(OP_SUCCESS, 'error')
                return render_json(return_dict)
            else:
                return_dict = build_ret_data(OP_SUCCESS, 'success')
                return render_json(return_dict)
        else:
            return_dict = build_ret_data(THROW_EXP, '序列化条件不满足')
            return render_json(return_dict)




