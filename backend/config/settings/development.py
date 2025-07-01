from dj_database_url import parse as dburl
from decouple import config
from pathlib import Path

from .base import *  # noqa: F403


INSTALLED_APPS += [  # noqa: F405
    # Development tools
    "django_extensions",
    "debug_toolbar",
]

DIR = BASE_DIR  # noqa: F405

default_dburl = f"sqlite:///{Path.joinpath(DIR, '../db.sqlite3').resolve()}"
DATABASES = {"default": config("DATABASE_URL", default=default_dburl, cast=dburl)}


# For Django Debug Toolbar
INTERNAL_IPS = ["127.0.0.1"]
