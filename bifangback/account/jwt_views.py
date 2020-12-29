from datetime import datetime
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework_jwt.views import RefreshJSONWebToken
from rest_framework_jwt.views import VerifyJSONWebToken
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomJwtBackend(ModelBackend):
    """
    自定义用户验证，定义完之后还需要在settings中进行配置
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            # django里面的password是加密的，前端传过来的password是明文，
            # 调用check_password就会对明文进行加密，比较两者是否相同
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 不改rest_framework_jwt源码的情况下，自定义登陆后成功和错误的返回，最优雅
def jwt_response_payload_handler(token, user=None, expiration=None):
    """
    自定义jwt认证成功返回数据
    """
    data = {
        'token': token,
        'expireAt': expiration,
        'user_id': user.id,
        'user': {
            'id': user.id,
            'name': user.username,
            'email': user.email,
            'avatar': ''},
        'is_superuser': user.is_superuser,
        'permissions': [{'id': 'queryForm', 'operation': ['add', 'edit']}],
        'roles': [{'id': 'admin', 'operation': ['add', 'edit', 'delete']}],
    }
    return {'code': 0, 'message': '欢迎回来', 'data': data}


def jwt_response_payload_error_handler(serializer, requst=None):
    """
    自定义jwt认证错误返回数据
    """
    data = {
        'message': "用户名或者密码错误",
        'status': 400,
        'detail': serializer.errors,
    }
    return {'code': -1, 'data': data}


# jwt的返回，由JSONWebTokenAPIView，自定义它的调用和返回即可
class CustomWebTokenAPIView(JSONWebTokenAPIView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            expiration = (datetime.utcnow() +
                          api_settings.JWT_EXPIRATION_DELTA)
            response_data = jwt_response_payload_handler(token, user, expiration)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expiration=expiration,
                                    httponly=True)
            return response
        error_data = jwt_response_payload_error_handler(serializer, request)
        return Response(error_data, status=status.HTTP_200_OK)


class CustomObtainJSONWebToken(ObtainJSONWebToken, CustomWebTokenAPIView):
    pass


class CustomRefreshJSONWebToken(RefreshJSONWebToken, CustomWebTokenAPIView):
    pass


class CustomVerifyJSONWebToken(VerifyJSONWebToken, CustomWebTokenAPIView):
    pass


obtain_jwt_token = CustomObtainJSONWebToken.as_view()
refresh_jwt_token = CustomRefreshJSONWebToken.as_view()
verity_jwt_token = CustomVerifyJSONWebToken.as_view()