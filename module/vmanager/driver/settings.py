# Copyright 2016-2017 certus Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from driver.pub.config import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3o-wney!99y)^h3v)0$j16l9=fdjxcb+a8g+q3tfbahcnu2b0o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # ========== default ==========
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # ========== default ==========

    # ========== framework ==========
    'rest_framework',
    # ========== framework ==========

    # ========== module ==========
    # 'driver.pub.database',
    'driver.interfaces',
    'vnfpkgm',
    # ========== module ==========
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'driver.urls'

WSGI_APPLICATION = 'driver.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',),

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser'
    )
}


DATABASES = {
    'default': {
        # default sqlite3
        # 'ENGINE': 'django.db.backends.mysql',
        # 'NAME': 'vmanager',
        # 'HOST': 'localhost',
        # 'USER': 'root',
        # 'PASSWORD':'password',

        'ENGINE': 'mysql.connector.django',
        'NAME': 'vnfpkgm',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
        # transaction control
        'ATOMIC_REQUESTS': True,
    }
}

# redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, password='', db=1)

# reconfig database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

TIME_ZONE = 'UTC'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s:[%(name)s]:[%(filename)s]-[%(lineno)d] [%(levelname)s]:%(message)s',
        },
    },
    'filters': {},
    'handlers': {
        'driver_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/runtime_driver.log'),
            'formatter': 'standard',
            'maxBytes': 1024 * 1024 * 50,
            'backupCount': 5,
        },
    },

    'loggers': {
        'driver': {
            'handlers': ['driver_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
        'vnfpkgm': {
            'handlers': ['driver_handler'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

if 'test' in sys.argv:
    config.REG_TO_MSB_WHEN_START = False
    REST_FRAMEWORK = {}
    import platform
    if platform.system() == 'Linux':
        TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
        TEST_OUTPUT_VERBOSE = True
        TEST_OUTPUT_DESCRIPTIONS = True
        TEST_OUTPUT_DIR = 'test-reports'
