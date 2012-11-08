# Django settings for rhic_serve project.

from mongoengine import connect
from mongoengine.connection import register_connection

from splice.common.settings import *

from splice.common import config

MONGO_DATABASE_NAME = config.CONFIG.get('rhic_serve', 'db_name')
MONGO_DATABASE_HOST = config.CONFIG.get('rhic_serve', 'db_host')
# Connect to the mongo db
connect(MONGO_DATABASE_NAME, alias=MONGO_DATABASE_NAME, tz_aware=True,
        host=MONGO_DATABASE_HOST)
register_connection('default', MONGO_DATABASE_NAME, host=MONGO_DATABASE_HOST)

# Custom test runner to work with Mongo
TEST_RUNNER = 'rhic_serve.common.tests.MongoTestRunner'

LOGIN_URL = '/ui/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'javascript',
)

MIDDLEWARE_CLASSES = \
    MIDDLEWARE_CLASSES + \
    ('rhic_serve.common.middleware.RestLoginMiddleware',)

ROOT_URLCONF = 'rhic_serve.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'rhic_serve.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/usr/lib/rhic_webui/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tastypie',
    'tastypie_mongoengine',
)
