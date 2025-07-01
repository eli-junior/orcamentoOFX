from ninja import NinjaAPI

api = NinjaAPI(
    title="Budget API",
    version="0.0.1",
    description="Personal Budget API. Documentation for endpoints is available at /docs/",
    docs_url="docs/",
    urls_namespace="api",
)

api.add_router(prefix="/health", router="backend.api.healthcheck.router")
api.add_router(
    prefix="/v1", router="backend.api.v1.routers.ofx_import.router", tags=["v1"]
)
