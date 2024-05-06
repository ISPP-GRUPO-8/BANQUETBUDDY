"""
Django settings for banquetBuddy project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from selenium.webdriver import Chrome
import os
from dotenv import load_dotenv


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

BASE_URL = "https://banquetbuddy.pythonanywhere.com"

DRIVER_PATH = os.path.join(BASE_DIR, "static", "driver", "chromedriver.exe")
# Sustituimos la siguiente línea por la que sigue a continuación cpara probar en local
# BASE_URL = 'http:localhost:8000'

DEFAULT_FROM_EMAIL = "banquetbuddyoficial@gmail.com"

# Configuración para enviar correos electrónicos
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "banquetbuddyoficial@gmail.com"
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = "banquetbuddyoficial@gmail.com"
DB_PASSWORD = os.environ.get("DB_PASSWORD")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
    "catering_particular",
    "phonenumber_field",
    "catering_owners",
    "catering_employees",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.ProtectCurriculumMiddleware",
]

ROOT_URLCONF = "banquetBuddy.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(
                BASE_DIR, "banquetBuddy/catering_owners/templates"
            ),  # Directorio de plantillas para catering_owners
            os.path.join(BASE_DIR, "banquetBuddy/catering_employees/templates"),
            os.path.join(BASE_DIR, "banquetBuddy/catering_particular/templates"),
            os.path.join(BASE_DIR, "banquetBuddy/core/templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.global_variable",
            ],
        },
    },
]

WSGI_APPLICATION = "banquetBuddy.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "ispp",
        "USER": "ispp",
        "PASSWORD": DB_PASSWORD,
        "HOST": "localhost",
        "PORT": "5432",
    },
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "banquetbuddyoficial@gmail.com"
EMAIL_HOST_PASSWORD = "zsqt bsae cayb atuk"


AUTHENTICATION_BACKENDS = ["core.backends.EmailBackend"]
AUTH_USER_MODEL = "core.CustomUser"

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}


WEBDRIVER_OPTIONS = {
    "executable_path": DRIVER_PATH,  # Ruta al archivo del controlador WebDriver
    "headless": True,  # Ejecución sin interfaz gráfica (opcional)
    # Otras opciones de configuración según tus necesidades
}


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Madrid"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = "/static/"

LOGIN_URL = "login"


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "static/images/logos"),
]

STRIPE_PUBLISHABLE_KEY = "pk_test_51OvizxD9TmIUzfvMF88OWTD25G6N3pvtYLdxwlN6LeYDmvFWLGAPUck5EJdpuKsVq1Y7pXJ3AvpCIT7KKPqPm8gl00DKrw7abp"
STRIPE_SECRET_KEY = "sk_test_51OvizxD9TmIUzfvMeNMZmtR2wwOstpKMFHm6vtSFXrIrfUDnrBMip7rTblbpbSeofcCBrwBdlrJ4Xos7TQ5a3CvE004zNaXTHT"
STRIPE_API_VERSION = "2022-08-01"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Media root
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
