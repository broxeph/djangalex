import os
import sys

import dj_database_url

DEBUG = os.environ.get('DEBUG', False)

if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['.ball.lol']
    PREPEND_WWW = True

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'registration',
    'bootstrap3',
    'home.apps.HomeConfig',
    'wineapp.apps.WineappConfig',
    'storages',
]

SITE_ID = 1  # registration package compatibility?
ACCOUNT_ACTIVATION_DAYS = 7  # One-week activation window
REGISTRATION_AUTO_LOGIN = True  # Automatically log the user in.

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangalex.urls'

LOGIN_REDIRECT_URL = '/wineapp/review/user'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'djangalex.wsgi.application'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Include jQuery with Bootstrap JavaScript
BOOTSTRAP3 = {'include_jquery': True}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if DEBUG:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    # S3/CloudFront
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_CLOUDFRONT_DOMAIN = 'd7g0p15isxilq.cloudfront.net'

    # Static asset configuration
    STATIC_LOCATION = 'static'
    STATIC_ROOT = f'/{STATIC_LOCATION}/'
    STATIC_URL = f'//{AWS_CLOUDFRONT_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'djangalex.storages.StaticStorage'

    # Media configuration
    MEDIA_LOCATION = 'media'
    MEDIA_ROOT = f'/{MEDIA_LOCATION}/'
    MEDIA_URL = f'//{AWS_CLOUDFRONT_DOMAIN}/{MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'djangalex.storages.MediaStorage'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'djangalex', 'static'),)

# Parse database configuration from $DATABASE_URL
DATABASES = {'default': dj_database_url.config()}
