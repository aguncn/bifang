import os
from django.conf import settings
from cmdb.models import App
from cmdb.models import Action
from utils.gitlab import gitlab_trigger
from utils.gitlab import pipeline_status
from cmdb.models import Release
from cmdb.models import ReleaseStatus
from .serializers import ReleaseBuildSerializer
from .serializers import ReleaseBuildStatusSerializer
from rest_framework.views import APIView
from utils.ret_code import *
from utils.permission import is_right
from utils.write_history import write_release_history


class ReleaseBuildView(APIView):
    """
    编译软件

    参数:
    app_name
    release_name
    git_branch
    """
    def post(self, request):
        # 序列化前端数据，并判断是否有效
        serializer = ReleaseBuildSerializer(data=request.data)
        if serializer.is_valid():
            ser_data = serializer.validated_data
            user = request.user
            app_name = ser_data['app_name']
            release_name = ser_data['release_name']
            git_branch = ser_data['git_branch']
            app = App.objects.get(name=app_name)
            zip_package_name = app.zip_package_name
            git_url = app.git.git_url
            git_access_token = app.git.git_token
            git_trigger_token = app.git_trigger_token
            project_id = app.git_app_id
            build_script = app.build_script
            deploy_script = app.deploy_script
            file_up_server = settings.FILE_UP_SERVER

            # 前端开发完成后开启权限测试
            action = Action.objects.get(name='Create')
            if not is_right(app.id, action.id, user):
                return_dict = build_ret_data(NOT_PERMISSION, '你无此应用的新建及建构发布单权限！')
                return render_json(return_dict)

            # 先触发编译，但由于编译时间较长，为防连接过期，异步一下，先返回id，再获取编译状态
            try:
                pipeline = gitlab_trigger(git_url, git_access_token,
                                          project_id, app_name, release_name,
                                          git_branch, git_trigger_token,
                                          build_script, deploy_script,
                                          zip_package_name, file_up_server)
            except Exception as e:
                print(e)
                return_dict = build_ret_data(THROW_EXP, 'gitlab触发错误，请确认gitlab连接，运行及配置正确')
                return render_json(return_dict)
            # 在编译前，更新一下发布单的状态，待写编译历史库记录
            release_status_name = 'Building'
            release_status = ReleaseStatus.objects.get(name=release_status_name)
            release = Release.objects.filter(name=release_name).update(pipeline_id=pipeline.id,
                                                                       pipeline_url=pipeline.web_url,
                                                                       release_status=release_status)
            write_release_history(release_name=release_name,
                                  env_name=None,
                                  release_status_name=release_status_name,
                                  deploy_type=None,
                                  log='Building',
                                  user_id=user.id)

            return_dict = build_ret_data(OP_SUCCESS, 'gitlab ci pipeline id: {}'.format(pipeline.id))
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
        # 序列化前端数据，并判断是否有效
        # 在获取状态时，前端可以不传pipeline id过来，因为这个id可以通过数据库获取
        serializer = ReleaseBuildStatusSerializer(data=request.data)
        if serializer.is_valid():
            ser_data = serializer.validated_data
            user = request.user
            app_name = ser_data['app_name']
            release_name = ser_data['release_name']
            app = App.objects.get(name=app_name)
            zip_package_name = app.zip_package_name
            deploy_script = app.deploy_script
            # 部署脚本在上传时，只取了最后的文件名，目录名被忽略，这里也要作转换
            deploy_script = os.path.basename(deploy_script)
            git_url = app.git.git_url
            git_access_token = app.git.git_token
            project_id = app.git_app_id
            release = Release.objects.get(name=release_name)
            pipeline_id = release.pipeline_id

            pipeline = pipeline_status(git_url, git_access_token, project_id, pipeline_id)
            if pipeline.finished_at is None:
                print(pipeline.status)
                return_dict = build_ret_data(OP_SUCCESS, 'ing')
                return render_json(return_dict)
            elif pipeline.status != 'success':
                print(pipeline)
                print(pipeline.id)
                print(pipeline.status)
                print(pipeline.ref)
                print(pipeline.web_url)
                print(pipeline.duration)
                release_status_name = 'BuildFailed'
                release_status = ReleaseStatus.objects.get(name=release_status_name)
                release = Release.objects.filter(name=release_name).update(release_status=release_status)
                write_release_history(release_name=release_name,
                                      env_name=None,
                                      release_status_name=release_status_name,
                                      deploy_type=None,
                                      log='Building',
                                      user_id=user.id)
                return_dict = build_ret_data(OP_SUCCESS, 'error')
                return render_json(return_dict)
            else:
                print(pipeline.status)
                file_down_server = settings.FILE_DOWN_SERVER
                deploy_script_url = '{}/{}/{}/{}'.format(file_down_server, app_name, release_name, deploy_script)
                zip_package_url = '{}/{}/{}/{}'.format(file_down_server, app_name, release_name, zip_package_name)
                release_status_name = 'Build'
                release_status = ReleaseStatus.objects.get(name=release_status_name)
                Release.objects.filter(name=release_name).update(release_status=release_status,
                                                                 deploy_script_url=deploy_script_url,
                                                                 zip_package_url=zip_package_url)
                write_release_history(release_name=release_name,
                                      env_name=None,
                                      release_status_name=release_status_name,
                                      deploy_type=None,
                                      log='Build',
                                      user_id=user.id)

                return_dict = build_ret_data(OP_SUCCESS, 'success')
                return render_json(return_dict)
        else:
            return_dict = build_ret_data(THROW_EXP, '序列化条件不满足')
            return render_json(return_dict)
