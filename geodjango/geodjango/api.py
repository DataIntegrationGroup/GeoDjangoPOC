from ninja import NinjaAPI

api = NinjaAPI()

api.add_router('/locations/', 'samplelocations.api.locations.router')
api.add_router('/wells/', 'samplelocations.api.wells.router')
api.add_router('/contacts/', 'samplelocations.api.contacts.router')