"""
Django settings for path2prep_backend project.

This file imports from settings/ directory based on environment.
"""
import os

# Determine which settings to use
ENVIRONMENT = os.environ.get('DJANGO_ENV', 'development')

if ENVIRONMENT == 'production':
    from .settings.production import *
else:
    from .settings.development import *
