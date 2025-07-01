from ninja import Router
from ninja.responses import Response
from ninja.errors import HttpError

from django.db import connection


router = Router(tags=["Health Check"])


@router.get("/status")
def health(request):
    return "UP!"


@router.get("/ready")
def ready(request):
    status_code = 200
    response = {"database": None}
    try:
        with connection.cursor() as cursor:
            cursor.execute("select 1")
    except Exception as e:
        response["database"] = str(e)
        status_code = 503
    else:
        response["database"] = "Ready"
    if status_code == 200:
        return Response(response)
    raise HttpError(status_code, str(response))
