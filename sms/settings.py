"""
Django settings for sms project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
# import django_heroku
from decouple import config
import dj_database_url
from pathlib import Path
# import cloudinary
# import cloudinary.uploader
# import cloudinary.api



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#zf41@8)=ii-0tcl6v+bfu#p77(wd$q2-iklx175#0&3wtswwo'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = ['0.0.0.0', 'localhost',
                 '127.0.0.1','https://sms-production-c4a6.up.railway.app','sms-production-c4a6.up.railway.app']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'cloudinary_storage',
    'django.contrib.staticfiles',
    #   'cloudinary',
    # third party apps
    'ckeditor',
    # 'ckeditor_uploader',
    
     "crispy_forms",
    'django_htmx',
    'rest_framework',
    'storages',
    # 'rest_framework.authtoken',
    # user apps
    "schoolinfo",
    'guardian',
    'student',
    'teacher',
    'adminhod',
    'fees',
    'library',
    
    'attendance',
    'marks',
    'blog',
    # 'apis',
    'timetable',
    
]


CRISPY_TEMPLATE_PACK='bootstrap4'
ROOT_URLCONF = "crispy_forms.tests.urls"
CRISPY_CLASS_CONVERTERS = {"textinput": "textinput textInput inputtext"}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
     "django_htmx.middleware.HtmxMiddleware",
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/"templates"],
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

WSGI_APPLICATION = 'sms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
# db_from_env = dj_database_url.config(conn_max_age=600)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'b6Y0ewdKKnr0o1GsA9MG',
        'HOST': 'containers-us-west-105.railway.app',
        'PORT': '7598'
    }
}

# DATABASES['default'].update(db_from_env)
# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# STATIC_URL = '/staticfiles/'

# STATICFILES_DIRS = [
#     BASE_DIR / "static",
#     '/var/www/static/',
# ]

# MEDIA_URL = '/media/'

# MEDIA_ROOT="media"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "adminhod.CustomUser"

# AUTHENTICATION_BACKENDS = [
#     "adminhod.EmailBackend.EmailBackEnds", 'django.contrib.auth.backends.ModelBackend']

AUTHENTICATION_BACKENDS = (
  
    # DEFAULT
    'django.contrib.auth.backends.ModelBackend',
    #EMAIL BACKEND
    'adminhod.EmailBackend.EmailBackEnds',
    # remot user
    'django.contrib.auth.backends.RemoteUserBackend',



)
LOGIN_URL = 'adminhod:login'
LOGIN_REDIRECT_URL = "adminhod:blog_home"
LOGOUT_REDIRECT_URL = "adminhod:login"
# AUTH_PROFILE_MODULE = "adminhod.CustomUser"

CKEDITOR_UPLOAD_PATH='blog/photos'


# for email


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "smsprogram0237@gmail.com"
EMAIL_HOST_PASSWORD = "nwecccnstosbvzbn" #real password='smsp24619'  app-password ="nwecccnstosbvzbn"
EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


AWS_ACCESS_KEY_ID = 'AKIAVBY2MECXTATDMX7H'
AWS_SECRET_ACCESS_KEY = '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'

AWS_STORAGE_BUCKET_NAME = 'smsprogram-storage'
AWS_S3_FILE_OVERWRITE=False
AWS_DEFAULT_ACL=None
AWS_S3_CUSTOM_DOMAIN = 'dcaezy3xv6q35.cloudfront.net'

AWS_LOCATION = 'static'
AWS_MEDIA_LOCATION = 'media'

STATIC_URL = '%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
MEDIAL_URL = '%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)


STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
     BASE_DIR / "static",
    # STATIC_URL,
]
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Debugging in heroku live
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = 'https://coder-miki.mo.cloudinary.net/rest/of/the/path/'
# cloudinary.config(
#     cloud_name="ceodiary",
#     api_key="889568188666134",
#     api_secret="DtgJDTAYRZT8VzFoVtGeyJHYB_Y"
# )

# LOUDINARY_URL=f'cloudinary://889568188666134:DtgJDTAYRZT8VzFoVtGeyJHYB_Y@ceodiary'

# DEBUG_PROPAGATE_EXCEPTIONS = True
# COMPRESS_ENABLED = os.environ.get('COMPRESS_ENABLED', False)

# MEDIA_URL = '/media/'  # or any prefix you choose
# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# django_heroku.settings(locals())