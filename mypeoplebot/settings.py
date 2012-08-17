# -*- coding: utf-8 -*-
# Django settings for mypeoplebot project.

import os
PROJECT_ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IS_LOCAL = 'Users' in PROJECT_ROOT_DIR
if IS_LOCAL:
    DEBUG = True
else:
    DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# custom settings - BIZONE
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

BOT_NAME = "bizone_bot"
if IS_LOCAL:
    BOT_CALLBACK_URL = "http://192.168.164.123:8000/callback/"
    oauth_callback_url= 'http://192.168.164.123:8000/oauth_callback/'
    consumer_key = '87058115-9053-41ad-97a2-232d5fc9c6f7'
    consumer_secret = 'YgLRV.sq11yibZaFnlPO1HzCXad_sjwSq47jbjTgOWugk8codkoDTA00'
else:
    BOT_CALLBACK_URL = "http://10.13.227.160/callback/"
    oauth_callback_url= 'http://10.13.227.160/oauth_callback/'
    consumer_key = 'cd1498d3-61a5-4e03-a98b-065c4212fd39'
    consumer_secret = 'kEVtfEi9tHPnJOmyW5p41BCFqcWNlNNUOJkYz3Sa7mFN53riEhU_6A00'

# ~custom settings - BIZONE

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': '/home/bizone/public_html/MyPeople-Psychological-Testing-Bot/mypeople',
        'NAME': 'mypeople',                      # Or path to database file if using sqlite3.
        'USER': 'mypeople',                      # Not used with sqlite3.
        'PASSWORD': 'mypeople',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Seoul'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ko-kr'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = PROJECT_ROOT_DIR + "/media/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# setting for compressor
COMPRESS_ENABLED = True
COMPRESS_ROOT = MEDIA_ROOT
COMPRESS_URL = MEDIA_URL

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = PROJECT_ROOT_DIR + '/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8(1cdw7y9e4gn)4uc@1^4$o8$28vsrp8js7y^h!8#ray)j)wdi'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mypeoplebot.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mypeoplebot.wsgi.application'

TEMPLATE_DIRS = (
    PROJECT_ROOT_DIR + "/templates",
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'wordbot',
    'pbutils',
    'django_extensions',
    'south',
    # Uncomment the next line to enable the admin:
    # 'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

import redis
redis_store = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

# Python에서 HTTP(S)통신을 하기위한 연결 정보입니다.
# apiServer는 API서비스를 제공하는 서버를 나타냅니다.
# apiPort는 API서비스를 제공하는서버의 서비스 포트를 나타냅니다.
# https방식(SSL)의 port는 443이며 http방식을 이용하고자 할땐 apiport를 80으로 설정합니다.
# Daum API는 SSL만 지원합니다.
api_server = 'apis.daum.net'
api_port = 443

# DaumAPI(OAuth)에 필요한 URL입니다. 
request_token_url = 'https://apis.daum.net/oauth/requestToken'
authorization_url = 'https://apis.daum.net/oauth/authorize'
access_token_url = 'https://apis.daum.net/oauth/accessToken'

# MyPeople연동에 필요한 URL입니다.
pb_register_url = 'https://apis.daum.net/mypeople/bot/register.json'
pb_edit_url = 'https://apis.daum.net/mypeople/profile/edit.json'
pb_buddy_send_url = 'https://apis.daum.net/mypeople/buddy/send.json'
