"""bifangback URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from account import jwt_views
from .views import index

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('jwt_auth/', jwt_views.obtain_jwt_token),
    path('refresh_jwt_auth/', jwt_views.refresh_jwt_token),
    path('verify_jwt_auth/', jwt_views.verity_jwt_token),
]

urlpatterns += [
    path('account/', include('account.urls')),
    path('app/', include('app.urls')),
    path('deploy/', include('deploy.urls')),
    path('env/', include('env.urls')),
    path('log/', include('log.urls')),
    path('release/', include('release.urls')),
    path('server/', include('server.urls')),
]