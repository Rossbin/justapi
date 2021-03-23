# 这是开发阶段配置文件


from .const import *   # 轮播图的配置文件导入

import os

# 现在BASE_DIR是内部的justapi
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 把这个路径加入到环境变量
import sys

# print(sys.path)
sys.path.insert(0, BASE_DIR)
# 把apps的路径加入到环境变量
sys.path.insert(1, os.path.join(BASE_DIR, 'apps'))
# print(sys.path)


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n+j19wk6mujfkffk@lx+!@($djlo6fw1gpzz!0@qa5wnx*@c7p'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    'rest_framework',
    'corsheaders',   # 第三方跨域
    'xadmin',        # xadmin主体模块
    'crispy_forms',  # 渲染表格模块
    'reversion',     # 为模型通过版本控制，可以回滚数据
    'django_filters',


    'user',  # 因为apps目录已经被加到环境变量了，所以能直接找到
    'home',
    'course',
    'order',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',  # 第三方跨域处理

    # 自己写的处理跨域CORS
    # 'justapi.utils.middle.MyMiddle',
]

ROOT_URLCONF = 'justapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'justapi.wsgi.application'

# Database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'justapi',
        'USER': 'justapi',
        'PASSWORD': 'just123?',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'CHARSET': 'utf-8'
    }
}
import pymysql

pymysql.install_as_MySQLdb()
# 上线后将密码放到环境变量中，在取出来
# 例如：password = sys.path.get('mysql_pass','123456')


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

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 现在的mediadir是justapi下的
# 配置自定义auth表
AUTH_USER_MODEL = 'user.user'

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'justapi.utils.exceptions.common_exceptions_handler',
}

# 日志的配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            # 实际开发建议使用WARNING
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            # 实际开发建议使用ERROR
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志位置,日志文件名,日志保存目录必须手动创建，注：这里的文件路径要注意BASE_DIR代表的是小justapi
            'filename': os.path.join(os.path.dirname(BASE_DIR), "logs", "just_error.log"),
            # 日志文件的最大值,这里我们设置300M
            'maxBytes': 300 * 1024 * 1024,
            # 日志文件的数量,设置最大日志数量为10
            'backupCount': 100,
            # 日志格式:详细格式
            'formatter': 'verbose',
            # 文件内容编码
            'encoding': 'utf-8'
        },
    },
    # 日志对象
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,  # 是否让日志信息继续冒泡给其他的日志处理系统
        },
    }
}

# 第三方跨域配置文件
CORS_ORIGIN_ALLOW_ALL = True
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
    'authorization',
    'content-type',
)


import datetime
JWT_AUTH = {        # JWT认证模块
    # token的过期时间7天
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),

}
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES':{      # 注册短信的频率
        'sms':'1/m'  # key要跟类中的scop对应
    }
}


# django默认不支持redis做缓存
# from django.core.cache.backends.filebased import FileBasedCache
# from django_redis.cache import RedisCache
# 缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
            # "PASSWORD": "123",
        }
    }
}




# 后台基URL
BASE_URL = 'http://127.0.0.1:8000'
# 前台基URL
LUFFY_URL = 'http://127.0.0.1:8080'
# 支付宝同步异步回调接口配置
# 后台异步回调接口  post
NOTIFY_URL = BASE_URL + "/order/success/"
# 前台同步回调接口，没有 / 结尾  get
RETURN_URL = LUFFY_URL + "/pay/success"