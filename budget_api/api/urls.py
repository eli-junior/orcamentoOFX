from ninja import NinjaAPI

# Routers are imported here
from .routers.lancamentos_router import router as lancamentos_router

# API instance for v1 business logic endpoints
# The docs_url will make swagger available at /api/v1/docs/
api_v1 = NinjaAPI(
    title="Budget API v1",
    version="1.0.0",
    description="Version 1 of the Personal Budget API. Documentation for v1 endpoints is available at /api/v1/docs/",
    docs_url="docs/",  # This will make docs available at the root of where api_v1 is mounted + /docs/
    urls_namespace="api_v1",
)


# Add routers to the api_v1 instance
api_v1.add_router(
    "/", lancamentos_router
)  # Mounts lancamentos_router endpoints at the root of /api/v1/

# Later, we will add more routers from api.views or dedicated router files here.
# For example:
# from .v1.routers.user_router import router as user_router # Example
# api_v1.add_router("/users", user_router)                   # Example
#
# from .v1.routers.budget_router import router as budget_router # Example
# api_v1.add_router("/budgets", budget_router)                   # Example

# The urlpatterns list in this file is not directly used by Django's URL resolver
# when api_v1.urls is included in the main config/urls.py.
# It's kept here by convention in some Django structures, but NinjaAPI objects
# are typically self-contained regarding their URL patterns via their .urls attribute.
urlpatterns = [
    # No Django URL patterns are typically defined here when using NinjaAPI's .urls attribute
    # for inclusion in the main urls.py.
]
