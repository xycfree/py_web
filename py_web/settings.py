"""
Django settings for py_web project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
import logging
import os
import sys
from datetime import datetime

import pymysql
from django.conf import global_settings

pymysql.install_as_MySQLdb()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# log_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 上级目录地址

log_dir = os.path.join(BASE_DIR, 'logs')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)  # 判断路径是否存在，不存在则创建路径

log_file = 'info-{}.log'.format(datetime.now().strftime('%Y-%m-%d'))  # 文件名
# log_file = 'info.log'  # 文件名
# log_err_file = 'error.log'  # 错误文件名
log_err_file = 'error-{}.log'.format(datetime.now().strftime('%Y-%m-%d'))


sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'xadmin'))
sys.path.insert(0, os.path.join(BASE_DIR, 'common'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$@-y$+y-d%=000f8abg@^-dryr2g71@rh!fj33skybabrkpar2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []
CSRF_COOKIE_SECURE = True
# AUTH 方法（支持邮箱登录）
AUTHENTICATION_BACKENDS = ('userinfo.views.CustomBackend',)

# UserProfile 覆盖了 django 内置的 user 表
AUTH_USER_MODEL = 'userinfo.UserProfile'  # 自定义AbstractUser来实现登录认证

# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',  # 有xadmin可以去掉
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'DjangoUeditor',  # 文章需要
    'userinfo',
    'xadmin',
    'crispy_forms',
    'captcha',
    'pure_pagination',
    'rest_framework',
    'snippets',
    'blog',
    'corsheaders',  # 白名单
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # 解决跨域
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]


ROOT_URLCONF = 'py_web.urls'
LOGIN_URL = '/login/'  # 这个路径需要根据你网站的实际登陆地址来设置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS':  [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 配置了这个之后，就会把最底下的  MEDIA_URL 注册到 html ，这样 html 就能用 MEDIA_URL 变量
                'django.template.context_processors.media',
                'django.template.context_processors.csrf',  # context processor csrf
            ],
        },
    },
]


WSGI_APPLICATION = 'py_web.wsgi.application'
# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pyweb',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 设置需要全局设置。在配置文件里，定义REST_FRAMEWORK,设置DEFAULT_PAGINATION_CLASS和PAGE_SIZE。
# 这样API会出现offset(开始位置)和limit(限制件数，default=PAGE_SIZE)等参数。
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny', ],

    # 如果想通过author来筛选Entry时。
    # 'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),
}

"""
在配置文件里添加DEFAULT_FILTER_BACKENDS。和分页所设置的是同一个字典。
class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    filter_fields = ('author', 'status')
然后在ViewSet里设置filter_fields。这样就可以通过author和status来筛选。 
API后面为?author=1，就会抽选User id=1的blog。?status=public会抽选已经公开的Blog 
其他筛选方法参照 http://www.django-rest-framework.org/api-guide/filtering/
"""




# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_TZ = True
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'


USE_I18N = True

USE_L10N = True

USE_TZ = False  # 数据库取本地时间


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 当运行 python manage.py collectstatic 的时候
# STATIC_ROOT 文件夹 是用来将所有 STATICFILES_DIRS 中所有文件夹中的文件，以及各 app 中 static 中的文件都复制过来
# 把这些文件放到一起是为了用 apache/nginx 等部署的时候更方便
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )


EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'xycfree@163.com'
EMAIL_HOST_PASSWORD = 'bingpoli123'
EMAIL_USE_TLS = False  # 一般都为False
EMAIL_FROM = 'xycfree@163.com'


# 跨域增加忽略
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    '*'
)

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            'format': '%(asctime)s [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        },
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            "formatter": "standard",
            'filename': os.path.join(log_dir, log_err_file),
            'mode': 'w+',
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 10,
            "encoding": "utf8",
        },

        "default": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "standard",
            "filename": os.path.join(log_dir, log_file),
            'mode': 'w+',
            "maxBytes": 1024 * 1024 * 50,  # 5 MB
            "backupCount": 10,
            "encoding": "utf8"
        },
        # 'celery': {
        #     'level': 'DEBUG',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': os.path.join(log_dir, 'celery.log'),
        #     'formatter': 'simple',
        #     'maxBytes': 1024 * 1024 * 50,  # 100 mb
        #     "backupCount": 10,
        #     "encoding": "utf8"
        # },
    },

    "loggers": {
        "app_name": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": "no"
        }
    },

    "root": {
        'handlers': ['default', 'console', 'error'],
        'level': "DEBUG",
        'propagate': False
    }
}

import logging.config
logging.config.dictConfig(LOGGING)
log = logging.getLogger(__name__)