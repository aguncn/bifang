from cmdb.models import Release
from .serializers import ReleaseSerializer
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
