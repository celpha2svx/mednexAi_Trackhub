from .base import *  # noqa

DEBUG = True

INSTALLED_APPS += ['debug_toolbar']  # noqa
MIDDLEWARE.insert(1, 'debug_toolbar.middleware.DebugToolbarMiddleware')  # noqa
INTERNAL_IPS = ['127.0.0.1']
