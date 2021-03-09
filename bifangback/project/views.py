from cmdb.models import Project
from .serializers import ProjectSerializer
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework.generics import DestroyAPIView
from utils.ret_code import *
from .filters import ProjectFilter


class ProjectListView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_class = ProjectFilter

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)


class ProjectCreateView(CreateAPIView):
    serializer_class = ProjectSerializer

    def post(self, request):
        """
        {
            "name": "projectA",
            "cn_name":"A项目",
            "description": "这是一个A项目",
            "project_id": 4325
        }
        """
        req_data = request.data
        data = dict()
        data['project_id'] = req_data['project_id']
        data['name'] = req_data['name']
        data['description'] = req_data['description']
        data['cn_name'] = req_data['cn_name']
        # data['project_id'] = req_data['project_id']
        # 从drf的request中获取用户(对django的request作了扩展的)
        data['create_user'] = request.user.id
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid() is False:
            return_dict = build_ret_data(THROW_EXP, str(serializer.errors))
            return render_json(return_dict)
        data = serializer.validated_data
        Project.objects.create(**data)
        return_dict = build_ret_data(OP_SUCCESS, serializer.data)
        return render_json(return_dict)


class ProjectRetrieveView(RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)


class ProjectUpdateView(UpdateAPIView):
    """
    url获取pk,修改时指定序列化类和query_set
    """
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    # 前端使用patch方法，到达这里
    def patch(self, request, *args, **kwargs):
        req_data = request.data
        pid = req_data['id']
        name = req_data['name']
        cn_name = req_data['cn_name']
        description = req_data['description']
        project_id = req_data['project_id']
        # 这样更新，可以把那些update_date字段自动更新，而使用filter().update()则是不会
        try:
            _p = Project.objects.get(id=pid)
            _p.name = name
            _p.cn_name = cn_name
            _p.description = description
            _p.project_id = project_id
            _p.save()
            return_dict = build_ret_data(OP_SUCCESS, str(req_data))
            return render_json(return_dict)
        except Exception as e:
            print(e)
            return_dict = build_ret_data(THROW_EXP, str(e))
            return render_json(return_dict)


class ProjectDestroyView(DestroyAPIView):
    queryset = Project.objects.all()

    def destroy(self, request, *args, **kwargs):
        try:
            res = super().destroy(self, request, *args, **kwargs)
            return_dict = build_ret_data(OP_SUCCESS, str(res))
            return render_json(return_dict)
        except Exception as e:
            print(e)
            return_dict = build_ret_data(THROW_EXP, str(e))
            return render_json(return_dict)
