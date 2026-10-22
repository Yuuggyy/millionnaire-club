"""
Configuration Django — Backend Limoncello (ex-Supabase).
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

<<<<<<< HEAD
import os
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-limoncello-local-dev-change-me-en-production")
DEBUG = os.environ.get("DJANGO_DEBUG", "True").lower() in ("1", "true", "yes")
STATIC_ROOT = BASE_DIR / "staticfiles"
=======
SECRET_KEY = "django-insecure-limoncello-local-dev-change-me-en-production"
DEBUG = True
>>>>>>> aeacd5e (Logo officiel du club : filigrane doré sur le papier du menu + logo en couverture (design épuré))

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "menuapp",
]

MIDDLEWARE = [
    "menuapp.cors.CorsApiMiddleware",  # CORS pour le front (surge.sh, VPS, etc.)
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "frontend"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
    # Pour MySQL (VPS) :
    # "default": {
    #     "ENGINE": "django.db.backends.mysql",
    #     "NAME": "limoncello",
    #     "USER": "limoncello",
    #     "PASSWORD": "à-remplir",
    #     "HOST": "127.0.0.1",
    #     "PORT": "3306",
    # }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Africa/Kinshasa"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "frontend"]  # build du front servi par Django
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Rediriger les logs HTTP inutiles en console
import logging  # noqa: E402
logging.getLogger("django.server").setLevel(logging.WARNING)
