from cmdb.models import Server
from .serializers import ServerSerializer
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import DestroyAPIView
from utils.ret_code import *
from .filters import ServerFilter


class ServerListView(ListAPIView):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    filter_class = ServerFilter

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)


class ServerCreateView(CreateAPIView):
    serializer_class = ServerSerializer

    def post(self, request):
        """
        {
            "name": "192.168.1.159-8080",
            "description": "这是一个服务器",
            "ip": "192.168.1.159",
            "port": 8080,
            "app_id": 1,
            "system_type": "LINUX"
        }
        """
        req_data = request.data
        data = dict()
        data['name'] = req_data['name']
        data['description'] = req_data['description']
        data['ip'] = req_data['ip']
        data['port'] = req_data['port']
        data['app'] = req_data['app_id']
        data['system_type'] = req_data['system_type']
        # 从drf的request中获取用户(对django的request作了扩展的)
        data['create_user'] = request.user.id
        serializer = ServerSerializer(data=data)
        if serializer.is_valid() is False:
            return_dict = build_ret_data(THROW_EXP, str(serializer.errors))
            return render_json(return_dict)
        data = serializer.validated_data
        Server.objects.create(**data)
        return_dict = build_ret_data(OP_SUCCESS, serializer.data)
        return render_json(return_dict)


class ServerRetrieveView(RetrieveAPIView):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)


class ServerUpdateView(UpdateAPIView):
    """
    url获取pk,修改时指定序列化类和query_set
    """
    serializer_class = ServerSerializer
    queryset = Server.objects.all()

    # 前端使用patch方法，到达这里
    def patch(self, request, *args, **kwargs):
        req_data = request.data
        pid = req_data['id']
        name = req_data['name']
        ip = req_data['ip']
        port = req_data['port']
        # 这样更新，可以把那些update_date字段自动更新，而使用filter().update()则是不会
        try:
            _s = Server.objects.get(id=pid)
            _s.ip = ip
            _s.port = port
            _s.name = name
            _s.save()
            return_dict = build_ret_data(OP_SUCCESS, str(req_data))
            return render_json(return_dict)
        except Exception as e:
            print(e)
            return_dict = build_ret_data(THROW_EXP, str(e))
            return render_json(return_dict)


class ServerDestroyView(DestroyAPIView):
    queryset = Server.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            res = super().destroy(self, request, *args, **kwargs)
            return_dict = build_ret_data(OP_SUCCESS, str(res))
            return render_json(return_dict)
        except Exception as e:
            print(e)
            return_dict = build_ret_data(THROW_EXP, str(e))
            return render_json(return_dict)
