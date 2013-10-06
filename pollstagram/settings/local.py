from .base import *
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'pollstagram.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

MEDIA_URL = ''

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    PROJECT_DIR.child('static'),
)

