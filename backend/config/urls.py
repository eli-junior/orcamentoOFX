"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path

# Import the v1 API instance from api/urls.py
from backend.api import api


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]

# Include debug toolbar URLs if DEBUG is True
if settings.DEBUG is True:
    try:
        import debug_toolbar
        from django.urls import include

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
