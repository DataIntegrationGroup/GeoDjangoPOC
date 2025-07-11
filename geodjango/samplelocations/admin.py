from django.contrib import admin
from django import forms
from django.contrib.gis.admin import GISModelAdmin
from django.contrib.gis.geos import Point
from samplelocations.models import Location, Thing, WellThing, SpringThing, Location_Thing_Junction, Sensor, Datastream, Observation, \
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
