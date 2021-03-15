from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from cmdb.models import App
from cmdb.models import Action
from cmdb.models import Permission
from .serializers import PermissionSerializer
from .filters import PermissionFilter
from utils.ret_code import *

User = get_user_model()


class PermissionListView(ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_class = PermissionFilter

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)


class PermissionCreateView(CreateAPIView):
    serializer_class = PermissionSerializer

    def post(self, request):
        """
        {
            "action": "Create",
            "user_id": 15,
            "app_name": "Ratings",
        }
        """
        req_data = request.data
        print(req_data, "@@@@@@@@@@@@")
        data = dict()
        user = User.objects.get(id=req_data['user_id'])
        app = App.objects.get(name=req_data['app_name'])
        action = Action.objects.get(name=req_data['action'])
        permission_name = '{}-{}-{}'.format(app.name, action.name, user.username)
        data['name'] = permission_name
        data['description'] = permission_name
        data['app'] = app.id
        data['action'] = action.id
        data['pm_user'] = user.id
        # 从drf的request中获取用户(对django的request作了扩展的)
        data['create_user'] = request.user.id
        serializer = PermissionSerializer(data=data)
        print(serializer)
        if serializer.is_valid() is False:
            print("!!!!!!!!!!!!!!!")
            return_dict = build_ret_data(THROW_EXP, str(serializer.errors))
            return render_json(return_dict)
        data = serializer.validated_data
        print(data, "&&&&&&&&&&&&&&&&&&&&")
        Permission.objects.create(**data)
        return_dict = build_ret_data(OP_SUCCESS, serializer.data)
        return render_json(return_dict)

