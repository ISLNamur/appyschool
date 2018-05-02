# This file is part of HappySchool.
#
# HappySchool is the legal property of its developers, whose names
# can be found in the AUTHORS file distributed with this source
# distribution.
#
# HappySchool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HappySchool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with HappySchool.  If not, see <http://www.gnu.org/licenses/>.

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')$g)mysea$a+_^mbzx$@!4lv_h$ecp@pp7a9g=%5ume#is6cg!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'channels',
    'channels_api',
    'crispy_forms',
    'core',
    # 'schedule_change',
    'webpack_loader',
    'annuaire',
    # 'infirmerie',
    # 'appels',
    # 'absence_prof',
    # 'dossier_eleve',
    # 'mail_notification',
    # 'mail_answer',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'happyschool.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.installed_apps.installed_apps',
            ],
        },
    },
]

WSGI_APPLICATION = 'happyschool.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'happyschool',
        'USER': 'happyschool',
        'PASSWORD': 'libreschool',
        'HOST': os.getenv("DB_HOST", "localhost"),
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static/"),
        'static/',
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

CRISPY_TEMPLATE_PACK = 'bootstrap3'

LOGIN_URL = 'auth'
LOGIN_REDIRECT_URL = 'annuaire'

EMAIL_ADMIN = os.getenv("EMAIL_ADMIN", "admin@example.org")

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.server.com")
EMAIL_PORT = os.getenv("EMAIL_PORT", 465)
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "admin@example.org")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "password")
EMAIL_FROM = os.getenv("EMAIL_FROM", "robot@example.org")

if EMAIL_PORT == 465:
    EMAIL_USE_SSL = True
elif EMAIL_PORT == 587:
    EMAIL_USE_TLS = True

USE_LDAP_INFO = True

LDAP_HOST = os.getenv("LDAP_HOST", "localhost")
LDAP_DOMAIN = os.getenv("LDAP_DOMAIN", "dc=example,dc=org")

# Use LDAP to authenticate
AUTH_LDAP_BIND_AS_AUTHENTICATING_USER = True
AUTH_LDAP_BIND_DN = os.getenv("LDAP_USER", "cn=admin,dc=example,dc=org")
AUTH_LDAP_BIND_PASSWORD = os.getenv("LDAP_PWD", "ldap_password")
AUTH_LDAP_SERVER_URI = "ldap://" + LDAP_HOST
if USE_LDAP_INFO:
    import ldap
    from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
    AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=people,%s" % LDAP_DOMAIN,
                                       ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

AUTH_LDAP_USER_ATTR_MAP = {"first_name": "cn", "last_name": "sn"}

groups = ['sysadmin', 'professeur', 'educateur', 'secretaire', 'accueil', 'pms']
active_groups = map(lambda g: "cn=%s,ou=groups,%s" % (g, LDAP_DOMAIN), groups)

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": list(active_groups),
    "is_staff": "cn=sysadmin,ou=groups,%s" % LDAP_DOMAIN,
    "is_superuser": "cn=sysadmin,ou=groups,%s" % LDAP_DOMAIN
    }

AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=groups,%s" % LDAP_DOMAIN,
                                        ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)"
                                    )
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="cn")
AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_MIRROR_GROUPS = True

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'fr-be'

TIME_ZONE = 'Europe/Brussels'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_INPUT_FORMATS = [
    '%H:%M:%S',     # '14:30:59'
    '%H:%M:%S.%f',  # '14:30:59.000200'
    '%H:%M',        # '14:30'
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

CELERY_NAME = "happyschool"
CELERY_BACKEND = "redis"
CELERY_BROKER = 'redis://localhost:6379'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_redis.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
        "ROUTING": "happyschool.routing.channel_routing",
    },
}

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}

MAILGUN_KEY = "your-mailgun-key"

MEDIA_SYNC = {
    'rsync_command': "/usr/bin/rsync -e ssh -avz --delete-after /home/user/happyschool/media happyschool@remote:/home/user/happyschool/",
}