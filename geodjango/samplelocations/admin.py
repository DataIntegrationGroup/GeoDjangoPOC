from django.contrib import admin
from unfold.admin import ModelAdmin 
from .models import SampleLocation, Owner, Contact, Well, Lexicon, WellScreen, Equipment, Spring 

@admin.register(SampleLocation)
class SampleLocationAdmin(ModelAdmin):
    pass

@admin.register(Owner)
class OwnerAdmin(ModelAdmin):
    pass

@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    pass

@admin.register(Lexicon)
class LexiconAdmin(ModelAdmin):
    pass

@admin.register(Well)
class WellAdmin(ModelAdmin):
    pass

@admin.register(WellScreen)
class WellScreenAdmin(ModelAdmin):
    pass

@admin.register(Equipment)
class EquipmentAdmin(ModelAdmin):
    pass

@admin.register(Spring)
class SpringAdmin(ModelAdmin):
    pass
