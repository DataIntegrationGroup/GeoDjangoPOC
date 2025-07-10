from django.contrib import admin
from .models import Location, Thing, WellThing, SpringThing, Location_Thing_Junction, Sensor, Datastream, Observation, \
    GroundwaterLevelObservation, Sample


admin.site.register(Location)
admin.site.register(Thing)
admin.site.register(WellThing)
admin.site.register(SpringThing)
admin.site.register(Location_Thing_Junction)
admin.site.register(Sensor)
admin.site.register(Datastream)
admin.site.register(Observation)
admin.site.register(GroundwaterLevelObservation)
admin.site.register(Sample)
#admin.site.register(Lexicon)
#admin.site.register(WellScreen)
#admin.site.register(Equipment)
#admin.site.register(Spring)
