"""
Django settings for EduLA project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-4h4#%$3-%0fn9qc!y$5le#j4e!z9v4tndl$ux9qa6xr^2)-y+)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "corsheaders",
    'colorfield',
    'admin_interface',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'EduGeneralApp',
    'EduAsistenteApp',
    'EduEstudianteApp',
    'DBConfigApp',
    'ModelCustomApp',
    'rest_framework',
    'sslserver',
    'drf_yasg',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ALGORITHM': 'HS256',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_HEADER_TYPES': ('Bearer',),
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'EduLA.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'EduLA/templates'),
            os.path.join(BASE_DIR, 'EduGeneralApp/templates'),
        ],
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

WSGI_APPLICATION = 'EduLA.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'DB/db.sqlite3',
    }
}
#configuracion para usar mongodb como base de datos
"""
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': '[db_nombre]',
        'CLIENT': {
            'host': 'mongodb://usuario:contraseña@host:puerto/db_nombre',
            'port': 27017
        }
    }
}
"""

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


#Cors
CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    'https://*.ngrok-free.app',
]
#autenticacion para login, tanto para el modelo User predeterminado de django y los customs
AUTHENTICATION_BACKENDS = [
    'EduEstudianteApp.backends.PerfilBackend', #validacion para mi apliacion que apunta a mi modelo perfil
    'django.contrib.auth.backends.ModelBackend',  # Si quieres seguir usando el modelo User de Django el predeterminado
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

#base url static files (Configuracion principal)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'EduLA/static')

#archivos estaticos por app
STATICFILES_DIRS = [
    #os.path.join(BASE_DIR, 'EduGeneralApp/static'),
]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CORS_ALLOW_CREDENTIALS = True
"""
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True"""


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
