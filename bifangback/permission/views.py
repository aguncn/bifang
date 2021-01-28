from rest_framework.generics import ListAPIView
from cmdb.models import Permission
from .serializers import PermissionSerializer
from .filters import PermissionFilter
from utils.ret_code import *


class PermissionListView(ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_class = PermissionFilter

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)

