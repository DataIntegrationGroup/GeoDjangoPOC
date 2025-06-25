from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    """
    A simple endpoint that returns a greeting.
    """
    return {"message": "Hello, GeoDjango!"}
