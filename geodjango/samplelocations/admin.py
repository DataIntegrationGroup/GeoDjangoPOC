from django.contrib import admin
from unfold.admin import ModelAdmin
from django import forms
from django.contrib.gis.admin import GISModelAdmin
from django.contrib.gis.geos import Point
from samplelocations.models import Location, Thing, Location_Thing_Junction, Sensor, Datastream, Observation, \
    GroundwaterLevelObservation, Sample

class LocationForm(forms.ModelForm):
    x = forms.FloatField(label="Longitude")
    y = forms.FloatField(label="Latitude")
    z = forms.FloatField(label="Elevation")


    class Meta:
        model = Location
        fields = ["x", "y", "z"]

    def save(self, commit=True):
        self.instance.coordinate = Point(self.cleaned_data["x"], self.cleaned_data["y"], self.cleaned_data["z"], srid=4326)
        return super().save(commit=commit)

@admin.register(Location)
class LocationAdmin(GISModelAdmin):
    form = LocationForm
    list_display = ("location_id", "coordinate", "date_created")

@admin.register(Thing)
class ThingAdmin(ModelAdmin):
    pass

@admin.register(Location_Thing_Junction)
class LocationThingJunctionAdmin(ModelAdmin):
    pass

@admin.register(Sensor)
class SensorAdmin(ModelAdmin):
    pass

@admin.register(Datastream)
class DatastreamAdmin(ModelAdmin):
    pass

@admin.register(Observation)
class ObservationAdmin(ModelAdmin):
    pass

@admin.register(GroundwaterLevelObservation)
class GroundwaterLevelObservationAdmin(ModelAdmin):
    pass

@admin.register(Sample)
class SampleAdmin(ModelAdmin):
    pass

# @admin.register(WellThing)
# class WellThingAdmin(ModelAdmin):
#     pass

# @admin.register(SpringThing)
# class SpringThingAdmin(ModelAdmin):
#     pass

#admin.site.register(Lexicon)
#admin.site.register(WellScreen)
#admin.site.register(Equipment)
#admin.site.register(Spring)
