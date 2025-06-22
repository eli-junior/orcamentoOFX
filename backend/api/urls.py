from ninja import NinjaAPI

# Routers are imported here
from .v1.routers.lancamentos_router import router as lancamentos_router

# API instance for v1 business logic endpoints
# The docs_url will make swagger available at /api/v1/docs/
api = NinjaAPI(
    title="Budget API v1",
    version="1.0.0",
    description="Personal Budget API. Documentation for v1 endpoints is available at /api/docs/",
    docs_url="docs/",  # This will make docs available at the root of where api_v1 is mounted + /docs/
    urls_namespace="api",
)


# Add routers to the api_v1 instance
api.add_router("/v1/", lancamentos_router, tags=["Version 1"])
