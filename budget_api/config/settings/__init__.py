# This file tells Django which settings module to use.
# By default, we point to development settings.
# You could use an environment variable (e.g., DJANGO_ENV)
# to switch between 'development' and 'production' dynamically.
#
# Example using an environment variable:
# from decouple import config
# DJANGO_ENV = config('DJANGO_ENV', default='development')
#
# if DJANGO_ENV == 'production':
#     from .production import *
# else:
#     from .development import *

from .development import *
