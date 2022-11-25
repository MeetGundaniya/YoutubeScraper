"""
Django settings for YoutubeScraper project.
"""

# STDLIB LIBRARY
import sys

# LOCALFOLDER LIBRARY
from . import BASE_DIR, env



# all django app fall under multiapps directory
sys.path.insert(0, BASE_DIR("multiapps"))

# all django settings and confg fall under backend directory
sys.path.insert(0, BASE_DIR("backend"))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG")


# List of host ip to searve this project
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")


# Application definition

INSTALLED_APPS = [
  "django.contrib.admin",
  "django.contrib.auth",
  "django.contrib.contenttypes",
  "django.contrib.sessions",
  "django.contrib.messages",
  "django.contrib.staticfiles",
  
  # local apps
  "core.apps.CoreConfig",
  "scraper.apps.ScraperConfig",
]

MIDDLEWARE = [
  "django.middleware.security.SecurityMiddleware",
  "django.contrib.sessions.middleware.SessionMiddleware",
  "django.middleware.common.CommonMiddleware",
  "django.middleware.csrf.CsrfViewMiddleware",
  "django.contrib.auth.middleware.AuthenticationMiddleware",
  "django.contrib.messages.middleware.MessageMiddleware",
  "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
  {
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
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

WSGI_APPLICATION = "backend.wsgi.application"


# Database settings

DATABASES = {
  "default": {},
  "mongodb": {
    "ENGINE": "djongo",
    "NAME": env.str('MONGO_DB_NAME'),
    "ENFORCE_SCHEMA": False,
    "CLIENT": {
      # pylint: disable-next=line-too-long
      "host": f"mongodb+srv://{env.str('MONGO_USERNAME')}:{env.str('MONGO_PASSWORD')}@{env.str('MONGO_CLUSTER')}\
        .phvbuke.mongodb.net/?retryWrites=true&w=majority"
    },
  },
}

DATABASE_ROUTERS = ["scraper.dbrouters.ScraperRouter"]


# Password validation

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Django logging

LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'formatters': {
    'verbose': {
      '()': 'backend.settings.log_formatter.ColoredFormatter',
      'colorize': True,
    },
    'simple': {
      '()': 'backend.settings.log_formatter.ColoredFormatter',
    },
  },
  'handlers': {
    'console': {
      'class': 'logging.StreamHandler',
      'formatter': 'verbose',
      'level': 'DEBUG',
    },
    'file': {
      'class': 'logging.FileHandler',
      'formatter': 'simple',
      'level': 'DEBUG',
      'filename': 'loggger.log',
    },
  },
  'loggers': {},
}


# Static files (CSS, JavaScript, Images)

STATIC_ROOT = BASE_DIR('assets', 'staticfiles')
STATIC_URL = "/assets/static/"


# Media files (Images, Video, etc)

MEDIA_ROOT = BASE_DIR("assets", "media")
MEDIA_URL = "/assets/media/"


# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



__all__ = sorted([i for i in dir() if i.isupper()])  # type: ignore
__all__ += ['env']
