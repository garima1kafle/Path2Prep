"""
Development settings
"""
from .base import *

DEBUG = True

# Allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True

# Database - can use SQLite for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Disable SSL for local development
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

