"""
Django settings for _United  project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

# pylint: disable-all
import os
import re
from pathlib import Path

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# INIT FIREBASE CONFIG
try:
    FIREBASE_CONFIG_FILE = os.path.join(
        BASE_DIR, "src/config/firebase/firebase-config.json"
    )
    cred = credentials.Certificate(FIREBASE_CONFIG_FILE)
    firebase_admin.initialize_app(cred)
except:
    print("CANNOT CONNECT FIREBASE")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition
# CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://sub.example.com",
    "http://localhost:3000",
]
# os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

ACTIVATE_JWT = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",  # for login admin site
    "django.contrib.staticfiles",  # for web design
    "api.Team",
    "api.Match",
    "api.Player",
    "api.UnitedMatch",
    "rest_framework",
    # "rest_framework.authtoken",
    "corsheaders",
    # "django_filters",
    "_United",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "_United.middlewares.JwtHandlerMiddleware",
]

DISALLOWED_USER_AGENTS = (re.compile(r"^Bingbot"), re.compile(r"^Googlebot"))


ROOT_URLCONF = "_United.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "static/templates/")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI_APPLICATION = "_United.wsgi.application"
# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Ho_Chi_Minh"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

APPEND_SLASH = True

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        # Active if you want to use jwt with local database
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    },
}

IS_LOGGING = False
LOGGING = (
    {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
            },
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": "django_queries.log",  # Choose a file name and path
            },
        },
        "loggers": {
            "django.db.backends": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }
    if IS_LOGGING
    else None
)


DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
