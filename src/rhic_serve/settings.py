# Django settings for rhic_serve project.

from mongoengine import connect
from mongoengine.connection import register_connection

from splice.common.settings import *

# Conditional imports for the various django apps that rhic-serve installs to
# see which ones are installed.
# We could use separate settings.py for each, but this seems easier for now.

try:
    from rhic_serve import rhic_rest
    has_rhic_rest = True
except ImportError:
    has_rhic_rest = False

try:
    from rhic_serve import rhic_webui
    has_rhic_webui = True
except ImportError:
    has_rhic_webui = False

try:
    from rhic_serve import rhic_rcs
    has_rhic_rcs = True
except ImportError:
    has_rhic_rcs = False

from splice.common import config

MONGO_DATABASE_NAME = config.CONFIG.get('rhic_serve', 'db_name')
# Connect to the mongo db
connect(MONGO_DATABASE_NAME, alias=MONGO_DATABASE_NAME, tz_aware=True)
register_connection('default', MONGO_DATABASE_NAME)

# Custom test runner to work with Mongo
TEST_RUNNER = 'rhic_serve.common.tests.MongoTestRunner'

AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)

SESSION_ENGINE = 'mongoengine.django.sessions'

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
    ('rhic_serve.common.middleware.RestLoginMiddleware',
    'rhic_serve.common.middleware.RestExceptionMiddleware')

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

if has_rhic_rest:
    INSTALLED_APPS += ('rhic_serve.rhic_rest', )
if has_rhic_webui:
    INSTALLED_APPS += ('rhic_serve.rhic_webui', )
if has_rhic_rcs:
    INSTALLED_APPS += ('rhic_serve.rhic_rcs', )
