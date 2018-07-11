# -*- coding: utf-8 -*-
from ConfigParser import RawConfigParser

config = RawConfigParser()
config.read('/usr/local/yatse/config/web.ini')

DEBUG = config.getboolean('debug','DEBUG')
#DEBUG_PROPAGATE_EXCEPTIONS = DEBUG
XMLRPC_DEBUG = False
ALLOWED_HOSTS = ['*']

USE_TZ = True
SITE_ID = 1

TESTSYTEM = config.getboolean('debug','TESTSYTEM')

ADMINS = tuple(config.items('admins'))
MANAGERS = ADMINS

EMAIL_SUBJECT_PREFIX = 'yatse-dev'
EMAIL_HOST = config.get('mail', 'EMAIL_HOST')
EMAIL_PORT = config.get('mail', 'EMAIL_PORT')
SERVER_EMAIL = config.get('mail', 'SERVER_EMAIL')
EMAIL_HOST_USER = config.get('mail', 'EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config.get('mail', 'EMAIL_HOST_PASSWORD')

#DATABASE_ROUTERS = ['web.routers.ModelRouter']
DATABASES = {
    'default': {
        'ENGINE': config.get('database', 'DATABASE_ENGINE'),
        'NAME': config.get('database', 'DATABASE_NAME'),
        'USER': config.get('database', 'DATABASE_USER'),
        'PASSWORD': config.get('database', 'DATABASE_PASSWORD'),
        'HOST': config.get('database', 'DATABASE_HOST'),
        'PORT': config.get('database', 'DATABASE_PORT'),
        'ATOMIC_REQUESTS': config.get('database', 'ATOMIC_REQUESTS')
    }
}

CACHES = {
    'default': {
        'BACKEND': config.get('cache', 'CACHE_BACKEND'),
        'LOCATION': '127.0.0.1:11211',
    }
}

#AUTH_PROFILE_MODULE = 'yatse.UserProfile'

TIME_ZONE = config.get('locale', 'TIME_ZONE')
LANGUAGE_CODE = config.get('locale', 'LANGUAGE_CODE')

gettext = lambda s: s
LANGUAGES = (
    ('de', gettext('German')),
    ('en', gettext('English')),
)
USE_I18N = True
USE_L10N = True

FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440 * 1024
FILE_UPLOAD_PATH = config.get('folder', 'FILE_UPLOAD_PATH')
FILE_UPLOAD_VIRUS_SCAN = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

STATIC_ROOT = config.get('folder', 'STATIC_ROOT')

# Absolute path to the directory temp files should be saved to.
# used for reports
TEMP_ROOT = '/tmp/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
MF_UI_URL = STATIC_URL

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ')ha6uuz1zqw3$r1-bqk1wv=wh%=*7aheo&6-cm(_z)v+bs%%!*'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.contrib.messages.context_processors.messages',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.tz',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
            ],
            'loaders': [
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'yatse.middleware.header.ResponseInjectHeader',
    #'yatse.middleware.auth.BasicAuthMiddleware',
    #'yatse.middleware.error.ErrorCaptureMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'web.urls'

WSGI_APPLICATION = 'web.wsgi.application'

TEMPLATE_DIRS = (
)

DEVSERVER_TRUNCATE_SQL = False
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'yatse',
    'bootstrap_toolkit',
    'oauth2_provider',
    'corsheaders',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'request_handler': {
                'level':'DEBUG',
                'class':'logging.handlers.RotatingFileHandler',
                'filename': config.get('folder', 'LOGGING_PATH'),
                'maxBytes': 1024*1024*5, # 5 MB
                'backupCount': 5,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['request_handler', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

TICKET_SEARCH_FIELDS = ['caption', 'c_user', 'priority', 'type', 'customer', 'component', 'deadline', 'billing_needed', 'billing_done', 'closed', 'assigned', 'state']
