from .base import *

ALLOWED_HOSTS = [
    'commercecore-production.up.railway.app'
]

CSRF_TRUSTED_ORIGINS = [
    "https://commercecore-production.up.railway.app",
    "https://commercecore-production.up.railway.app/",
]

DEBUG = True

# STATIC
# ------------------------
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATICFILES_DIRS = [os.path.join(BASE_DIR.parent, 'static')]
STATIC_ROOT = '/app/staticfiles'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
# SECURE_SSL_REDIRECT = False
