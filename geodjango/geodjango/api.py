from ninja import NinjaAPI, Redoc

api = NinjaAPI(docs=Redoc())

api.add_router('/locations', 'samplelocations.api.locations.router')
api.add_router('/wells', 'samplelocations.api.wells.router')
api.add_router('/contacts', 'samplelocations.api.contacts.router')