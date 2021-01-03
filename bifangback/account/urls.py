from django.urls import include, path
from rest_framework import routers
from .user_group_views import UserViewSet, GroupViewSet
from .views import UpdatePasswordView
from .views import UpdateEmailView
from .views import ForgetPasswordView
from .views import ResetPasswordView
from .views import UserRegisterView

# 使用router注册view，绑定url映射关系，
# 关于什么时候使用router，什么时候不能使用，后面奖路由的时候在深入了解吧
router = routers.DefaultRouter()
router.register(r'users', UserViewSet) # 绑定view到users路由下
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('update_password/', UpdatePasswordView.as_view(), name='update_password'),
    path('update_email/', UpdateEmailView.as_view(), name='update_email'),
    path('forget_password/', ForgetPasswordView.as_view(), name='forget_password'),
    path('reset_password/', ResetPasswordView.as_view(), name='reset_password'),
]
