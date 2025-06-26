from .base import *  # noqa: F403

INSTALLED_APPS += [  # noqa: F405
    # Development tools
    "django_extensions",
    "debug_toolbar",
]


default_dburl = f"sqlite:///{Path.joinpath(BASE_DIR, '../db.sqlite3').resolve()}"
DATABASES = {"default": config("DATABASE_URL", default=default_dburl, cast=dburl)}


# For Django Debug Toolbar
INTERNAL_IPS = ["127.0.0.1"]
