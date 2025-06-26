from .base import *  # noqa: F403


DATABASES = {"default": config("DATABASE_URL", cast=dburl)}
