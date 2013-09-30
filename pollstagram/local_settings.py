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

MEDIA_ROOT = ''
MEDIA_URL = ''
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static'),
)
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates'),
)