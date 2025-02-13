# Define config vars and Register app in INSTALLED APPS
from pathlib import Path

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS = ["*"]


INSTALLED_PLUGINS = [
    "tinymce",
    "registration",
    "crispy_forms",
    "crispy_bootstrap5",
    "versatileimagefield",
    "django_recaptcha",
    "dal",
    "dal_select2",
]


DJANGO_APPS = [
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


MODULES = [
    "web",
    "accounts",
    "order",
    "main",
    "products",
]

INSTALLED_APPS = INSTALLED_PLUGINS + DJANGO_APPS + MODULES

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.admindocs.middleware.XViewMiddleware",
]


ROOT_URLCONF = "balad.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "web.context_processors.main_context",
            ],
        },
    },
]


WSGI_APPLICATION = "balad.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": config("DB_NAME", default=BASE_DIR / "db.sqlite3"),
        "USER": config("DB_USER", default=""),
        "PASSWORD": config("DB_PASSWORD", default=""),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": "5432",
        "OPTIONS": {},
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators


AUTH_PASSWORD_VALIDATORS = [
    # {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    # {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# TINYMCE_JS_URL = "https://cdn.tiny.cloud/1/no-api-key/tinymce/6/tinymce.min.js"
# TINYMCE_COMPRESSOR = False

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

USE_L10N = False
DATE_INPUT_FORMATS = (
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%d/%m/%y",
    "%d %b %Y",
    "%d %b, %Y",
    "%d %b %Y",
    "%d %b, %Y",
    "%d %B, %Y",
    "%d %B %Y",
)
DATETIME_INPUT_FORMATS = (
    "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y %H:%M",
    "%d/%m/%Y",
    "%d/%m/%y %H:%M:%S",
    "%d/%m/%y %H:%M",
    "%d/%m/%y",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d",
)

VERSATILEIMAGEFIELD_SETTINGS = {
    "cache_length": 2592000,
    "cache_name": "versatileimagefield_cache",
    "jpeg_resize_quality": 70,
    "sized_directory_name": "__sized__",
    "filtered_directory_name": "__filtered__",
    "placeholder_directory_name": "__placeholder__",
    "create_images_on_demand": True,
    "image_key_post_processor": None,
    "progressive_jpeg": False,
}

X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
STATIC_URL = "/static/"
STATIC_FILE_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = ((BASE_DIR / "static"),)
STATIC_ROOT = BASE_DIR / "assets"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True

REGISTRATION_OPEN = True
LOGIN_URL = "/accounts/login/"
LOGOUT_URL = "/accounts/logout/"
LOGIN_REDIRECT_URL = "/"


EMAIL_BACKEND = config("EMAIL_BACKEND")
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


SESSION_COOKIE_SECURE = True
# DOMAIN = "http://127.0.0.1:8000"
DOMAIN = "https://balad.geany.website"

RAZOR_PAY_KEY = config("RAZOR_PAY_KEY")
RAZOR_PAY_SECRET = config("RAZOR_PAY_SECRET")


RECAPTCHA_PUBLIC_KEY = "6Lf_EqApAAAAAJHsDpM3jMUGs4PPfSUd58eqL5DG"
RECAPTCHA_PRIVATE_KEY = "6Lf_EqApAAAAABjw2eBv9pUGIxFZIjDj3F0d5ga7"


TINYMCE_DEFAULT_CONFIG = {
    "height": 500,
    "width": 900,
    "plugins": "link image preview codesample table fullscreen",
    "toolbar": "undo redo | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image | codesample | table | fullscreen",
    "menubar": "file edit view insert format tools table",
    "content_style": "body { font-family:Arial,sans-serif; font-size:14px }",
}

TINYMCE_JS_URL = "/static/tinymce/tinymce.min.js"
TINYMCE_JS_ROOT = "/static/tinymce"
