from .base import *

DEBUG = os.environ.get('DEBUG')

# INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS

ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
    "localhost:8080",
    "localhost:5173",
    "127.0.0.1:5173"
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8080',
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]

SECURE_BROWSER_XSS_FILTER = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '143621340002-lmgf8f4tb5i5blkdt3hptkb5fsk6930m.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = 'http://127.0.0.1:8000/accounts/google/login/callback/'
# LOGIN_REDIRECT_URL = 'http://127.0.0.1:8000/accounts/google/login/callback/'
# LOGOUT_REDIRECT_URL = 'http://127.0.0.1:8000/accounts/google/login/callback/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.knowbintech.com'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
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

DELHIVERY_API_KEY = os.environ.get('DELHIVERY_API_KEY')




