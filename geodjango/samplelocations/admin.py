from django.contrib import admin
from .models import SampleLocation, Owner, Contact, Well, Lexicon, WellScreen, Equipment, Spring 

admin.site.register(SampleLocation)
admin.site.register(Owner)
admin.site.register(Contact)
admin.site.register(Lexicon)
admin.site.register(Well)
admin.site.register(WellScreen)
admin.site.register(Equipment)
admin.site.register(Spring)
