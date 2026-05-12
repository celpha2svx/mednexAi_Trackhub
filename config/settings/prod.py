from .base import *  # noqa

DEBUG = False

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),         # noqa
        'USER': env('DB_USER'),         # noqa
        'PASSWORD': env('DB_PASSWORD'), # noqa
        'HOST': env('DB_HOST'),         # noqa
        'PORT': env('DB_PORT', default='5432'),  # noqa
        'CONN_MAX_AGE': 60,
    }
}
