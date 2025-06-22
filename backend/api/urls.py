from backend.api import api
from backend.api.v1.routers.hello import router as v1_hello_router
from backend.api.healthcheck import router as heathcheck_router



api.add_router("/v1/", v1_hello_router, tags=["Version 1"])
api.add_router("/", heathcheck_router, tags=["Health Check"])
