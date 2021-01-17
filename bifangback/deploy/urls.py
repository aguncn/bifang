from django.urls import path
from . import deploy_views
from django.views.decorators.csrf import csrf_exempt

app_name = "deploy"

urlpatterns = [
    # csrf_exempt用在这里，deploy异步视图才会生效，不然，得注释settings里的CsrfViewMiddleware
    path('deploy/', csrf_exempt(deploy_views.deploy), name='deploy'),
]
