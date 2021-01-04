from cmdb.models import Env
from .serializers import EnvSerializer
from rest_framework.generics import ListAPIView
from utils.ret_code import *
from .filters import EnvFilter


class EnvListView(ListAPIView):
    queryset = Env.objects.all()
    serializer_class = EnvSerializer
    filter_class = EnvFilter

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)
