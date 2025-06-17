from .base import *
from decouple import config # Ensure config is available if not already through base

DEBUG = config('DEBUG', default=True, cast=bool)

# In this setup, django_extensions and debug_toolbar are already in base.py's INSTALLED_APPS.
# If they were conditional, you might add them here:
# INSTALLED_APPS_DEV = [
#     'django_extensions',
#     'debug_toolbar',
# ]
# INSTALLED_APPS = INSTALLED_APPS + [app for app in INSTALLED_APPS_DEV if app not in INSTALLED_APPS]

# Add any other development-specific settings here
# For example, email backend for development:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
