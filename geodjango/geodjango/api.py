from ninja import NinjaAPI

api = NinjaAPI()

api.add_router('/samplelocations/', 'samplelocations.api.router')