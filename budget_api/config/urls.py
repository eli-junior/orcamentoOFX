"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include # include is used for debug_toolbar
from django.conf import settings
from ninja import NinjaAPI
from django.db import connection
from django.http import JsonResponse

# Import the v1 API instance from api/urls.py
from api.urls import api_v1

# Public API instance (health checks, etc.)
public_api = NinjaAPI(
    title="Budget API - Public",
    description="Public and health check endpoints. API documentation for these endpoints is available at /public/docs/.",
    version="1.0.0",
    docs_url="docs/", # Docs will be at /public/docs/
    urls_namespace="public_api"
)

@public_api.get("/health", tags=["Health"], summary="Health Check", description="Returns UP! if the service is running.")
def health_check(request):
    """
    Simple health check endpoint to confirm the API service is running.
    """
    return JsonResponse({"status": "UP!"})

@public_api.get("/ready", tags=["Health"], summary="Readiness Probe", description="Checks if the service is ready to handle requests, including database connectivity.")
def readiness_probe(request):
    """
    Readiness probe to check if the service is ready to handle requests.
    This includes checking for database connectivity.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            row = cursor.fetchone()
            if row is None or row[0] != 1:
                raise Exception("Database did not return expected value from SELECT 1")
        return JsonResponse({"status": "UP", "database": "OK"})
    except Exception as e:
        return JsonResponse({"status": "DOWN", "database": "Error", "details": str(e)}, status=503)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('public/', public_api.urls),    # Mounts /public/health, /public/ready, and /public/docs/
    path('api/v1/', api_v1.urls),      # Mounts all v1 endpoints (like /api/v1/sample) and v1 docs at /api/v1/docs/
]

# Include debug toolbar URLs if DEBUG is True
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
