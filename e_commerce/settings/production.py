from .base import *

DEBUG = os.environ.get('DEBUG')

INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS

ALLOWED_HOSTS = [
    "localhost:5173",
    "127.0.0.1:5173",
    "localhost:8080",
    "127.0.0.1:8080",
    "manage.signupcasuals.com:8443",
    "manage.signupcasuals.com",
    "signupcasuals.com",
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:8080',
    'http://127.0.0.1:8080',
    'https://manage.signupcasuals.com:8443',
    'https://manage.signupcasuals.com',
    'https://signupcasuals.com',
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'https://manage.signupcasuals.com:8443',
    'https://manage.signupcasuals.com',
    'https://signupcasuals.com',
]

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = False

# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = False

# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True

# X_FRAME_OPTIONS = 'DENY'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '143621340002-lmgf8f4tb5i5blkdt3hptkb5fsk6930m.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'
# SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = 'http://127.0.0.1:8000/accounts/google/login/callback/'
# LOGIN_REDIRECT_URL = 'http://127.0.0.1:8000/accounts/google/login/callback/'
# LOGOUT_REDIRECT_URL = 'http://127.0.0.1:8000/accounts/google/login/callback/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.knowbintech.com'
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False


USER_ID = os.environ.get('PHONE_PE_USER_ID')
MERCHANT_KEY = os.environ.get('PHONE_PE_MERCHANT_ID')
API_KEY = os.environ.get('PHONE_PE_API_KEY')
KEY_INDEX = os.environ.get('PHONE_PE_KEY_INDEX')

PHONE_PAY_S2S_CALLBACK_URL = os.environ.get('PHONE_PAY_S2S_CALLBACK_URL')
PHONE_PAY_REDIRECT_URL = os.environ.get('PHONE_PAY_REDIRECT_URL')

SHIPROCKET_EMAIL = os.environ.get('SHIPROCKET_EMAIL')
SHIPROCKET_PASSWORD = os.environ.get('SHIPROCKET_PASSWORD')

# SECURE_BROWSER_XSS_FILTER = False
# SECURE_REFERRER_POLICY = None
