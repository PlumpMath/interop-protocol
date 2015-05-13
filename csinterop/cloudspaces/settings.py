"""
Django settings for csinterop project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sybl!-=&c+7&!f%@c!c@yl6r)akne%)_48!rdm5f9i0r&p)4wu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'bootstrap3',
    'django_pg',
    'csinterop',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'cloudspaces.urls'

WSGI_APPLICATION = 'cloudspaces.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'stacksync_db',
        'USER': 'stacksync_user',
        'PASSWORD': 'stacksync_pass',
        'HOST': '10.30.233.214',
        'PORT': '5432',
    }
}

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.ModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    #'DEFAULT_PERMISSION_CLASSES': [
    #    'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    #]
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

SYNCSERVICE_IP = '127.0.0.1'
SYNCSERVICE_PORT = 61234

#OAuth Authentication Server
BASE_URL = "http://10.30.233.214:8080/oauth"
CLIENT_KEY = "b3af4e669daf880fb16563e6f36051b105188d413"
CLIENT_SECRET = "c168e65c18d75b35d8999b534a3776cf"
REQUEST_TOKEN_ENDPOINT = "/request_token"
ACCESS_TOKEN_ENDPOINT = "/access_token"
STACKSYNC_AUTHORIZE_ENDPOINT = "/authorize"

