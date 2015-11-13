"""
Django settings for purepython project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# WSGI_DIR = os.path.dirname(BASE_DIR)
# REPO_DIR = os.path.dirname(WSGI_DIR)
# DATA_DIR = os.environ.get('OPENSHIFT_DATA_DIR', BASE_DIR)
DJ_PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(DJ_PROJECT_DIR)
WSGI_DIR = os.path.dirname(BASE_DIR)
REPO_DIR = os.path.dirname(WSGI_DIR)
DATA_DIR = os.environ.get('OPENSHIFT_DATA_DIR', BASE_DIR)


# a setting to determine whether we are running on OpenShift
ON_OPENSHIFT = False
if os.environ.has_key('OPENSHIFT_REPO_DIR'):
    ON_OPENSHIFT = True
if os.environ.has_key('OPENSHIFT_APP_NAME'):
    DB_NAME = os.environ['OPENSHIFT_APP_NAME']
if os.environ.has_key('OPENSHIFT_POSTGRESQL_DB_USERNAME'):
    DB_USER = os.environ['OPENSHIFT_POSTGRESQL_DB_USERNAME']
if os.environ.has_key('OPENSHIFT_POSTGRESQL_DB_PASSWORD'):
    DB_PASSWD = os.environ['OPENSHIFT_POSTGRESQL_DB_PASSWORD']
if os.environ.has_key('OPENSHIFT_POSTGRESQL_DB_HOST'):
    DB_HOST = os.environ['OPENSHIFT_POSTGRESQL_DB_HOST']
if os.environ.has_key('OPENSHIFT_POSTGRESQL_DB_PORT'):
    DB_PORT = os.environ['OPENSHIFT_POSTGRESQL_DB_PORT']


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=^j)gy=u=y^z$#1&j*=!b9=cz$_j)+u0^3wttm(=07vhmhbik4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    ('Alex Buicescu', 'alex.buicescu@indyvision.net'),
)
MANAGERS = ADMINS

from socket import gethostname
ALLOWED_HOSTS = [
    gethostname(), # For internal OpenShift load balancer security purposes.
    os.environ.get('OPENSHIFT_APP_DNS'), # Dynamically map to the OpenShift gear name.
    #'example.com', # First DNS alias (set up in the app)
    #'www.example.com', # Second DNS alias (set up in the app)
    'notificationfilter-notifteam.rhcloud.com',
    'http://notificationfilter-notifteam.rhcloud.com',
    'https://notificationfilter-notifteam.rhcloud.com',
    'www.notificationfilter-notifteam.rhcloud.com',
    'http://www.notificationfilter-notifteam.rhcloud.com',
    'https://www.notificationfilter-notifteam.rhcloud.com',
]

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fb',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
)

ROOT_URLCONF = 'purepython.urls'

WSGI_APPLICATION = 'purepython.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

if ON_OPENSHIFT:
    # os.environ['OPENSHIFT_DB_*'] variables can be used with databases created
    # with rhc app cartridge add (see /README in this git repo)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': DB_NAME,               # Or path to database file if using sqlite3.
            'USER': DB_USER,               # Not used with sqlite3.
            'PASSWORD': DB_PASSWD,         # Not used with sqlite3.
            'HOST': DB_HOST,               # Set to empty string for localhost. Not used with sqlite3.
            'PORT': DB_PORT,               # Set to empty string for default. Not used with sqlite3.
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': os.path.join(DATA_DIR, 'sqlite3.db'),  # Or path to database file if using sqlite3.
            'USER': '',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(DATA_DIR, 'db.sqlite3'),
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Bucharest'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(WSGI_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


AVATAR_DEFAULT = 'img/avatar-placeholder.svg'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler'
#         }
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     }
# }