"""
Development settings
"""
from .base import *

DEBUG = True

# Allow all origins in development
CORS_ALLOW_ALL_ORIGINS = True

# Database - use SQLite for development (override base settings)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Override MongoDB settings for development (optional)
MONGODB_SETTINGS = {
    'host': 'localhost',
    'port': 27017,
    'db': 'path2prep_raw',
    'username': '',
    'password': '',
}

# Disable SSL for local development
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

