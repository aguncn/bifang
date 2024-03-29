"""
Django settings for bifangback project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!^s-#q3um$^8e6!&rc21(n0lj&m##6k=731*dp+l(c9znkaiv_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'account.apps.AccountConfig',
    'app.apps.AppConfig',
    'project.apps.ProjectConfig',
    'cmdb.apps.CmdbConfig',
    'deploy.apps.DeployConfig',
    'env.apps.EnvConfig',
    'gitapp.apps.GitappConfig',
    'history.apps.HistoryConfig',
    'release.apps.ReleaseConfig',
    'server.apps.ServerConfig',
    'permission.apps.PermissionConfig',
    'stats.apps.StatsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'drf_yasg',
    'simple_history',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'bifangback.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bifangback.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

"""
# 安装好mysqlclient之后(使用whl文件安装)，可以切换为mysql数据库
DATABASES = {
 'default': {
  'ENGINE': 'django.db.backends.mysql',
  'NAME': 'bifang',
  'USER': 'root',
  'PASSWORD': 'password',
  'HOST': '127.0.0.1',
  'PORT': '3306',
  'OPTIONS': {
    'charset': 'utf8mb4',
    # 'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
  }
 }
}
"""

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

CORS_ORIGIN_WHITELIST = [
    "https://example.com",
    "https://sub.example.com",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'utils.pagination.PNPagination',
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

# 自定义obtain_jwt_token登录参数验证
AUTHENTICATION_BACKENDS = (
    'account.jwt_views.CustomJwtBackend',
)
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=365),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
    'JWT_ALLOW_REFRESH': True,
}

# Django的redis缓存配置，性能要求高和有持久化要求时，可开启
# CACHES = {
#    "default": {
#        "BACKEND": "django_redis.cache.RedisCache",
#        "LOCATION": "redis://127.0.0.1:6379/1",
#        "OPTIONS": {
#            "CLIENT_CLASS": "django_redis.client.DefaultClient",
#        }
#    }
# }

# 邮件发送到控制台，而不发送到实际的邮箱
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# 正式使用时的邮箱设置
# EMAIL_USE_SSL = True
# EMAIL_HOST = 'smtp.163.com'
# EMAIL_PORT = 465
# EMAIL_HOST_USER = 'aguncn@163.com'
# EMAIL_HOST_PASSWORD = 'xxxxxxx'
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SIMPLE_HISTORY_REVERT_DISABLED = True

FILE_UP_SERVER = 'http://192.168.1.211:9001/upload-file'
FILE_DOWN_SERVER = 'http://192.168.1.211:9002'

