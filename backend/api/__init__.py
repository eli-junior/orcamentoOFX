from ninja import NinjaAPI

api = NinjaAPI(
    title="Budget API",
    version="0.0.1",
    description="Personal Budget API. Documentation for endpoints is available at /docs/",
    docs_url="docs/",
    urls_namespace="api",
)