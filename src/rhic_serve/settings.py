# Django settings for rhic_serve project.

from mongoengine import connect
from mongoengine.connection import register_connection

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


MONGO_DATABASE_NAME = 'rhic_serve'
# Connect to the mongo db
connect(MONGO_DATABASE_NAME, alias=MONGO_DATABASE_NAME, tz_aware=True)
register_connection('default', MONGO_DATABASE_NAME)

# Custom test runner to work with Mongo
TEST_RUNNER = 'rhic_serve.common.tests.MongoTestRunner'

CA_CERT_PATH = '/etc/pki/rhic-serve/rhic-serve-ca.crt'
CA_KEY_PATH = '/etc/pki/rhic-serve/rhic-serve-ca.key'
CERT_DAYS = 10000

AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)

SESSION_ENGINE = 'mongoengine.django.sessions'

TASTYPIE_FULL_DEBUG = True

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

LOGIN_URL = '/ui/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

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
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'javascript',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'trn+0rxgy+gy=2b4%lur@eha2ho!)!zt#e$63zq@i%#7prcf(e'

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

    'rhic_serve.common.middleware.RestLoginMiddleware',
    'rhic_serve.common.middleware.RestExceptionMiddleware',
)

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

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'stderr': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'level': 'INFO'
        },
    },
    'loggers': {
        'rhic_serve': {
            'handlers': ['stderr'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}

