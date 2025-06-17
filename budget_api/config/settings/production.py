from .base import *
from decouple import config # Ensure config is available if not already through base

DEBUG = config('DEBUG', default=False, cast=bool)

# Add production-specific settings below.
# For example:
# SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
# CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
# SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
# SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int) # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool)
# SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=bool)

# Ensure ALLOWED_HOSTS is properly set in production via environment variable
# Example: ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv()) # Already in base.py, but ensure it's not overridden by default "[]"

# Logging configuration for production
# Example:
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'root': {
#         'handlers': ['console'],
#         'level': 'WARNING',
#     },
# }

# Static files handling for production (e.g., WhiteNoise or S3)
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' # Example for WhiteNoise
