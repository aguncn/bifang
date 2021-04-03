from cmdb.models import Env
from cmdb.models import Release
from cmdb.models import Action
from cmdb.models import ReleaseStatus
from .serializers import EnvSerializer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from utils.ret_code import *
from .serializers import EnvExchangeSerializer
from .filters import EnvFilter
from utils.permission import is_right
from utils.write_history import write_release_history


class EnvListView(ListAPIView):
    queryset = Env.objects.all()
    serializer_class = EnvSerializer
    filter_class = EnvFilter

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)


class EnvExchangeView(APIView):
    """
    环境流转

    参数:
    env_id
    release_name
    app_id
    """
    def post(self, request):
        # 序列化前端数据，并判断是否有效
        serializer = EnvExchangeSerializer(data=request.data)
        if serializer.is_valid():
            ser_data = serializer.validated_data
            user = request.user
            release_name = ser_data['release_name']
            env_id = ser_data['env_id']
            env = Env.objects.get(id=env_id)
            app_id = ser_data['app_id']
            # 前端开发完成后开启权限测试
            action = Action.objects.get(name='Env')
            if not is_right(app_id, action.id, user):
                return_dict = build_ret_data(NOT_PERMISSION, '你无权在此应用下新建发布单！')
                return render_json(return_dict)

            release_status_name = 'Ready'
            release_status = ReleaseStatus.objects.get(name=release_status_name)
            release = Release.objects.filter(name=release_name).update(env=env,
                                                                       release_status=release_status)
            write_release_history(release_name=release_name,
                                  env_name=env.name,
                                  release_status_name=release_status_name,
                                  deploy_type=None,
                                  log='target env is {}.'.format(env.name),
                                  user_id=user.id)

            return_dict = build_ret_data(OP_SUCCESS, 'env exchange is ok.')
            return render_json(return_dict)
        else:
            return_dict = build_ret_data(THROW_EXP, '序列化条件不满足')
            return render_json(return_dict)

