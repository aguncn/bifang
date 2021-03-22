from cmdb.models import GitTb
from .serializers import GitappSerializer
from rest_framework.generics import ListAPIView
from utils.ret_code import *


class GitappListView(ListAPIView):
    queryset = GitTb.objects.all()
    serializer_class = GitappSerializer

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)
