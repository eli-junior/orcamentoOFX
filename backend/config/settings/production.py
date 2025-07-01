from dj_database_url import parse as dburl
from decouple import config

from .base import *  # noqa: F403

DATABASES = {"default": config("DATABASE_URL", cast=dburl)}
