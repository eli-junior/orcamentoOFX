from .base import *  # noqa: F403

INSTALLED_APPS += [  # noqa: F405
    # Development tools
    "django_extensions",
    "debug_toolbar",
]

# For Django Debug Toolbar
INTERNAL_IPS = ["127.0.0.1"]
