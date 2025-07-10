from django.contrib.gis.db import models

#--------Location model -----------

class Location(models.Model):
    """Represents a point location on the earth's surface"""
    location_id = models.BigAutoField(primary_key=True)
    point = models.PointField(
        srid=4326, #TODO: Did we come to a consensus on srid?
        spatial_index=True,
        dim=3, # Enable storage of Z data, e.g. elevation
        db_comment= "Defines the (X,Y,Z) coordinates of a location" # Comment on the database field. Stored at the db level.
    )
    date_created= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Location" # human-readable, singular name to the model. This name is used by Django in various contexts, most notably in the Django admin interface.
        verbose_name_plural = "Locations"
        db_table_comment = "This table stores point locations on the earth's surface" # Comment on the database table. Stored at the database level. Intended for individuals with direct database access who may not be working in the Django codebase.


#--------Thing model -----------

class Thing(models.Model):
    """A base model representing a generic monitoring station (Thing)"""
    thing_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    release_status = models.BooleanField(default=False) #TODO: What information does this field capture?
    date_created = models.DateTimeField(auto_now_add=True)
    # The 'location' field specifies the M:M relationship and specifies
    # the 'Locoation_Thing_Juncation' as the intermediate table.
    location = models.ManyToManyField(
        Location,
        through="Location_Thing_Junction", # specify the intermediate model to manage the many-to-many relationship.
        related_name="things", # define the reverse relationship for backend logic and database queries.
        verbose_name= "related location" # Human-readable label for user interfaces like forms and the admin panel.
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Thing"
        verbose_name_plural = "Things"


#--------Junction model for the Location and Thing models -----------

class Location_Thing_Junction(models.Model):
    """A junction model linking a Thing to a Location"""
    # Define a 1:M relationship using models.ForeignKey.
    # Django appends "_id" to FK field names (https://docs.djangoproject.com/en/5.2/ref/models/fields/#database-representation)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name= "locations",
        verbose_name= "related location"
    )
    thing = models.ForeignKey(
        Thing,
        on_delete=models.CASCADE,
        related_name= "things",
        verbose_name= "related thing"
    )

    # Define composite primary key. A composite primary key, when defined using
    # CompositePrimaryKey, is considered a virtual field.
    pk = models.CompositePrimaryKey("location_id", "thing_id")

    # Additional fields
    effective_start = models.DateTimeField()
    effective_end = models.DateTimeField()

    def __str__(self):
        return f"{self.location} - {self.thing}"

    class Meta:
        db_table_comment = "Junction table linking Location and Thing models"


#--------WellThing model. Inherits all fields from Thing model -----------
class WellThing(Thing):
    """A specific type of monitoring station (Thing)."""
    # This field creates the inheritance link from WellThing back to Thing.
    thing_ptr= models.OneToOneField(Thing, parent_link = True, related_name='things', verbose_name="related thing", on_delete=models.CASCADE)
    well_depth = models.FloatField(blank=True, null=True, help_text="feet below ground surface")
    hole_depth = models.FloatField(blank=True, null=True, help_text="feet below ground surface")
    casing_diameter = models.FloatField(blank=True, null=True, help_text="inches")
    casing_depth = models.FloatField(blank=True, null=True, help_text="feet below ground surface")
    casing_description = models.CharField(max_length=50, blank=True, null=True)
    construction_notes = models.TextField(blank=True, null=True) # It is recommended to use TextField over CharField for text of variable and potentially large size

    def __str__(self):
        return f"Well at {self.location.point}"

class WellScreen(models.Model):
    well = models.ForeignKey(Well, related_name='screens', on_delete=models.CASCADE)
    screen_depth_top = models.FloatField(help_text="feet below ground surface")
    screen_depth_bottom = models.FloatField(help_text="feet below ground surface")
    screen_type = models.ForeignKey(Lexicon, related_name='well_screens_by_type', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"Screen {self.screen_depth_top}-{self.screen_depth_bottom} ft for {self.well}"

class Equipment(models.Model):
    equipment_type = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial_no = models.CharField(max_length=50)
    date_installed = models.DateTimeField(blank=True, null=True)
    date_removed = models.DateTimeField(blank=True, null=True)
    recording_interval = models.IntegerField(blank=True, null=True)
    equipment_notes = models.CharField(max_length=50, blank=True, null=True)
    location = models.ForeignKey(SampleLocation, related_name='equipment', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.equipment_type} ({self.serial_no}) at {self.location.name}"

class Spring(models.Model):
    description = models.CharField(max_length=255, blank=True, null=True)
    location = models.ForeignKey(SampleLocation, related_name='springs', on_delete=models.CASCADE)

    def __str__(self):
        return f"Spring at {self.location.name}"