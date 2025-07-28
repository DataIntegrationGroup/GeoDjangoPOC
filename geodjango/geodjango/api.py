from ninja import NinjaAPI, Redoc

api = NinjaAPI()

# api.add_router('/locations', 'samplelocations.api.locations.router', tags=['locations'])
# api.add_router('/wells', 'samplelocations.api.wells.router', tags=['wells'])
# api.add_router('/contacts', 'samplelocations.api.contacts.router', tags=['contacts'])
api.add_router('/things', 'samplelocations.api.thing.router', tags=['things'])