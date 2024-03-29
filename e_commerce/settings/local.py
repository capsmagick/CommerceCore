from .base import *

DEBUG = os.environ.get('DEBUG')

INSTALLED_APPS = ["whitenoise.runserver_nostatic"] + INSTALLED_APPS

ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
    "localhost:8080",
    "localhost:5173",
    "127.0.0.1:5173"
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8080',
    'http://localhost',
    'http://localhost:8080/',
    'http://localhost:8081',
    'http://localhost:8000',
    'http://127.0.0.1:8008',
    'http://localhost:8008',
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]

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
LOGIN_REDIRECT_URL = 'http://127.0.0.1:8000/accounts/google/login/callback/'
LOGOUT_REDIRECT_URL = 'http://127.0.0.1:8000/accounts/google/login/callback/'

X_FRAME_OPTIONS = 'SAMEORIGIN'

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
