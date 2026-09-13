import os
import sys

import dj_database_url

DEBUG = os.environ.get('DEBUG', '').lower() == 'true'

if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['.ball.lol']
    PREPEND_WWW = True
    # The site is HTTPS-only (Cloudflare redirects HTTP), so never send cookies in the clear
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

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
    'django_extensions',
    'django_bootstrap5',
    'home.apps.HomeConfig',
    'wineapp.apps.WineappConfig',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
                'djangalex.context_processors.analytics',
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
USE_TZ = True

# Google Analytics 4 measurement ID (G-XXXXXXXXXX); analytics is disabled when unset
GA_MEASUREMENT_ID = os.environ.get('GA_MEASUREMENT_ID', '')

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static files: collected into staticfiles/ at build time and served by WhiteNoise
# (Cloudflare caches them at the edge). Hashed filenames make them immutable, so no CDN purges.
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'djangalex', 'static'),)

if DEBUG:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    # Uploaded media lives on S3 and is served through CloudFront
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_CLOUDFRONT_DOMAIN = 'd7g0p15isxilq.cloudfront.net'

    MEDIA_LOCATION = 'media'
    MEDIA_ROOT = f'/{MEDIA_LOCATION}/'
    MEDIA_URL = f'//{AWS_CLOUDFRONT_DOMAIN}/{MEDIA_LOCATION}/'

    STORAGES = {
        'default': {'BACKEND': 'djangalex.storages.MediaStorage'},
        'staticfiles': {'BACKEND': 'djangalex.storages.StaticStorage'},
    }

# Parse database configuration from $DATABASE_URL
DATABASES = {'default': dj_database_url.config()}

# Existing tables use 32-bit auto PKs; keep that rather than migrating to BigAutoField
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
