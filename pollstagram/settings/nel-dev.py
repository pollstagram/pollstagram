from .base import *
import os

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mrpoate@gmail.com'
EMAIL_HOST_PASSWORD = os.environ['nel_password']
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEBUG = True
