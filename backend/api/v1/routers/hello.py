from . import router


@router.get("hello")
def hello(request):
    return "World"