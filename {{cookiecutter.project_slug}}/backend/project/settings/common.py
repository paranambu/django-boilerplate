import os
import sys
import warnings

from django.utils.translation import gettext_lazy as _

import environ

root_dir = environ.Path(__file__) - 4
base_dir = root_dir.path('backend')
live_dir = root_dir.path('.live')

PROJECT_ALIAS = 'project'
PROJECT_DISPLAY_NAME = 'Project'

# Defaults
env = environ.Env(
    ADMINS=(list, []),
    DEBUG=(bool, False),
    SHOW_DEBUG_TOOLBAR=(bool, False),
    LOAD_EXTERNAL_REFS=(bool, True),
    REDIS_URL=(str, 'redis://localhost:6379/0'),
    USE_S3=(bool, False),
    DEFAULT_FROM_EMAIL=(str, 'info@localhost'),
    SERVER_EMAIL=(str, 'root@localhost'),
    EMAIL_HOST=(str, 'localhost'),
    EMAIL_HOST_PASSWORD=(str, ''),
    EMAIL_HOST_USER=(str, ''),
    EMAIL_PORT=(int, 25),
    EMAIL_USE_TLS=(bool, False),
    EMAIL_USE_SSL=(bool, False),
    EMAIL_SUBJECT_PREFIX=(str, PROJECT_DISPLAY_NAME),
    EMAIL_USE_CONSOLE=(bool, False),
    DATABASE_HOST=(str, 'localhost'),
    DATABASE_PORT=(str, ''),
    DATABASE_MAX_CONNS=(int, 20),
)

environ.Env.read_env(root_dir('.env'))
sys.path.append(base_dir('apps'))

DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = ['*']
INTERNAL_IPS = (
    '127.0.0.1',
    '0.0.0.0',
)
SITE_ID = 1

INSTALLED_APPS = [
    'polymorphic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'debug_toolbar',
    'hijack',
    'compat',

    'webpack_loader',
    'corsheaders',
    'widget_tweaks',
    'parler',
    'channels',
    'floppyforms',

    'users',
    'utils',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]


# =============================================================================
# Templates
# =============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            base_dir('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ALLOWABLE_TEMPLATE_SETTINGS = ('DEBUG', 'LOAD_EXTERNAL_REFS', 'PROJECT_DISPLAY_NAME')

HTML_MINIFY = not DEBUG


# =============================================================================
# Debug toolbar
# =============================================================================

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda req: DEBUG and env('SHOW_DEBUG_TOOLBAR'),
}

# =============================================================================
# Database
# =============================================================================

# CONN_MAX_AGE must be set to 0, or connections will never go back to the pool
DATABASES = {
    'default': {
        'ENGINE': 'django_db_geventpool.backends.postgresql_psycopg2',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
        'ATOMIC_REQUESTS': False,
        'CONN_MAX_AGE': 0,
        'OPTIONS': {
            'MAX_CONNS': env('DATABASE_MAX_CONNS'),
        },
    }
}


# =============================================================================
# Auth
# =============================================================================

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

AUTH_USER_MODEL = 'users.User'
LOGIN_REDIRECT_URL = '/'


# =============================================================================
# i18n/l10n
# =============================================================================

LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('en', _('English')),
]

LOCALE_PATHS = [base_dir('locale')]

PARLER_LANGUAGES = {
    SITE_ID: (
        {'code': 'en',},
    ),
}

# =============================================================================
# Static and media
# =============================================================================

STATICFILES_DIRS = [
    root_dir('frontend/.build'),
]

if env('USE_S3'):
    # TODO
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_QUERYSTRING_AUTH = False

    STATICFILES_LOCATION = 'static'
    STATIC_URL = 'https://s3.amazonaws.com/{}/{}/'.format(
        AWS_STORAGE_BUCKET_NAME, STATICFILES_LOCATION)
    STATICFILES_STORAGE = 'project.storages.StaticStorage'

    MEDIAFILES_LOCATION = 'media'
    MEDIA_URL = 'https://s3.amazonaws.com/{}/{}/'.format(
        AWS_STORAGE_BUCKET_NAME, MEDIAFILES_LOCATION)
    DEFAULT_FILE_STORAGE = 'project.storages.MediaStorage'
else:
    STATIC_ROOT = live_dir('static')
    STATIC_URL = '/static/'

    MEDIA_ROOT = live_dir('media')
    MEDIA_URL = '/media/'

    if not DEBUG:
        # Add WhiteNoiseMiddleware immediately after SecurityMiddleware
        index = MIDDLEWARE.index('django.middleware.security.SecurityMiddleware')
        MIDDLEWARE[index + 1] = 'whitenoise.middleware.WhiteNoiseMiddleware'

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': '',
        'STATS_FILE': root_dir('frontend/webpack-stats.json'),
    }
}

LOAD_EXTERNAL_REFS = env('LOAD_EXTERNAL_REFS')


# =============================================================================
# Hijack
# =============================================================================

HIJACK_LOGIN_REDIRECT_URL = '/admin/'
HIJACK_LOGOUT_REDIRECT_URL = HIJACK_LOGIN_REDIRECT_URL
HIJACK_ALLOW_GET_REQUESTS = True


# =============================================================================
# Mailing
# =============================================================================

EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_USE_SSL = env('EMAIL_USE_SSL')
EMAIL_SUBJECT_PREFIX = env('EMAIL_SUBJECT_PREFIX')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

# Email to send error messages
SERVER_EMAIL = env('SERVER_EMAIL')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
if env('EMAIL_USE_CONSOLE'):
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# =============================================================================
# Caches
# =============================================================================

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}


# =============================================================================
# Celery
# =============================================================================

CELERY_BROKER_URL = env('REDIS_URL')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = TIME_ZONE
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_MAX_CONNECTIONS = 1
CELERY_BROKER_POOL_LIMIT = 3
CELERYD_CONCURRENCY = 1


# =============================================================================
# Fixtures
# =============================================================================

FIXTURE_DIRS = [
    base_dir('fixtures'),
]

# See apps/utils/management/pushfixtures.py
FIXTURES = [
    #'{}/app_name.Model.csv'.format(FIXTURE_DIRS[0]),
]


# =============================================================================
# General
# =============================================================================

ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'
ASGI_APPLICATION = "project.asgi.application"

ADMINS = []
admins = env('ADMINS')
for admin in admins:
    ADMINS.append(admin.split(':'))

CORS_ORIGIN_ALLOW_ALL = True

# https://github.com/gregmuellegger/django-floppyforms/issues/172
# https://github.com/gregmuellegger/django-floppyforms/issues/189
warnings.filterwarnings('ignore', module='floppyforms', message='Unable to import floppyforms.gis')
