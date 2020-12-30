from django.urls import include, path
from rest_framework import routers
from .user_group_views import UserViewSet, GroupViewSet

# 使用router注册view，绑定url映射关系，
# 关于什么时候使用router，什么时候不能使用，后面奖路由的时候在深入了解吧
router = routers.DefaultRouter()
router.register(r'users', UserViewSet) # 绑定view到users路由下
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
