from rest_framework.generics import ListAPIView
from cmdb.models import ReleaseHistory
from cmdb.models import ServerHistory
from .filters import ReleaseHistoryFilter
from .filters import ServerHistoryFilter
from .serializers import ReleaseHistorySerializer
from .serializers import ServerHistorySerializer


from utils.ret_code import *


class ReleaseHistoryListView(ListAPIView):
    queryset = ReleaseHistory.objects.all()
    serializer_class = ReleaseHistorySerializer
    filter_class = ReleaseHistoryFilter

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)


class ServerHistoryListView(ListAPIView):
    queryset = ServerHistory.objects.all()
    serializer_class = ServerHistorySerializer
    filter_class = ServerHistoryFilter

    def get(self, request, *args, **kwargs):
        res = super().get(self, request, *args, **kwargs)
        return_dict = build_ret_data(OP_SUCCESS, res.data)
        return render_json(return_dict)

