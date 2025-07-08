from ninja import NinjaAPI, Redoc

api = NinjaAPI(docs=Redoc())

api.add_router('/locations', 'samplelocations.api.locations.router', tags=['locations'])
api.add_router('/wells', 'samplelocations.api.wells.router', tags=['wells'])
api.add_router('/contacts', 'samplelocations.api.contacts.router', tags=['contacts'])