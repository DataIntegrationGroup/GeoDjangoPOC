from django.contrib.gis.db import models

#--------Location model -----------

#TODO: Additional admin configuration is needed for this model. The admin panel currently
# displays a text box for the coordinate field and it is unclear what format is expected.
# I've read a few things about widgets being helpful here.

class Location(models.Model):
    """Represents a point location on the earth's surface"""
    location_id = models.BigAutoField(primary_key=True)
    coordinate = models.PointField(
        srid=4326,
        spatial_index=True,
        dim=3, # Enable storage of Z data, e.g. elevation
    )
    date_created= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.location_id

    class Meta:
        verbose_name = "Location" # human-readable, singular name to the model. This name is used by Django in various contexts, most notably in the Django admin interface.
        verbose_name_plural = "Locations"
        db_table_comment = "This table stores point locations on the earth's surface" # Comment on the database table. Stored at the database level. Intended for individuals with direct database access who may not be working in the Django codebase.


#--------Thing model -----------

class Thing(models.Model):
    """A base model representing a generic monitoring station (Thing)"""
    thing_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    release_status = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    # The 'location' field sets up the M:M relationship and specifies
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


#--------Junction model linking the Location and Thing models -----------

class Location_Thing_Junction(models.Model):
    """A junction model linking a Thing to a Location"""
    # Define a 1:M relationship using models.ForeignKey().
    # Django appends "_id" to FK field names (https://docs.djangoproject.com/en/5.2/ref/models/fields/#database-representation)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name= "locations_things",
        verbose_name= "related location"
    )
    thing = models.ForeignKey(
        Thing,
        on_delete=models.CASCADE,
        related_name= "locations_things",
        verbose_name= "related thing"
    )
      # Additional fields
    effective_start = models.DateTimeField()
    effective_end = models.DateTimeField()

    def __str__(self):
        return f"{self.location} - {self.thing}"

    class Meta:
        # This enforces that the combination of 'location' and 'thing' must be unique. This acts as a composite
        # primary key for the purpose of uniqueness, while still using the default 'id' field as the actual primary
        # key, which is necessary for the Django admin to work correctly.
        constraints = [
            models.UniqueConstraint(fields=["location", "thing"], name="unique_location_thing")
        ]
        db_table_comment = "Junction table linking Location and Thing models"


#--------WellThing model. Inherits all fields from Thing model -----------

class WellThing(Thing):
    """ A specific type of monitoring station (Thing) representing a well."""
    wellthing_id = models.BigAutoField(primary_key=True)
    # This field creates the inheritance link from WellThing back to Thing.
    # The name 'thing_ptr' is a conventional naming choice in Django for the parent link field,
    thing_ptr= models.OneToOneField(
        Thing,
        on_delete=models.CASCADE,
        parent_link = True,
        related_name='wellthings',
        verbose_name="related thing"
    )
    well_depth = models.FloatField(blank=True, null=True, help_text="feet below ground surface")
    hole_depth = models.FloatField(blank=True, null=True, help_text="feet below ground surface")
    casing_diameter = models.FloatField(blank=True, null=True, help_text="inches")
    casing_depth = models.FloatField(blank=True, null=True, help_text="feet below ground surface")
    casing_description = models.CharField(max_length=50, blank=True, null=True)
    construction_notes = models.TextField(blank=True, null=True) # Use TextField over CharField for long-form text of variable length without a predefined limit.

    def __str__(self):
        return f"{self.name} (Well)"


#--------SpringThing model. Inherits all fields from Thing model -----------

class SpringThing(Thing):
    """ A specific type of monitoring station (Thing) representing a spring."""
    springthing_id = models.BigAutoField(primary_key=True)
    # This field creates the inheritance link from SpringThing back to Thing.
    # The name 'thing_ptr' is a conventional naming choice in Django for the parent link field,
    thing_ptr = models.OneToOneField(
        Thing,
        on_delete=models.CASCADE,
        parent_link=True,
        related_name='springthings',
        verbose_name="related thing"
    )
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} (Spring)"


#--------Sensor model-----------

class Sensor(models.Model):
    sensor_id = models.BigAutoField(primary_key=True)
    serial_number = models.CharField(max_length=50, blank=True, null=True)
    install_date = models.DateTimeField(blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Sensor {self.serial_number} ({self.model})"


#--------Datastream (Series) model-----------

class Datastream(models.Model):
    """ A collection of observations from a Thing collected using a Sensor."""
    datastream_id = models.BigAutoField(primary_key=True)
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE, related_name="datastreams", verbose_name="related thing")
    sensor_id = models.OneToOneField(Sensor, on_delete=models.CASCADE, related_name="datastreams", verbose_name="related sensor")
    observed_property = models.CharField(max_length=100)
    release_status = models.BooleanField(default=False)


#--------Sample model-----------

class Sample(models.Model):
    """Represents a sample collected from a Thing"""
    sample_id = models.BigAutoField(primary_key=True)
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE, related_name="samples", verbose_name="related thing")
    sample_date = models.DateTimeField()
    sample_notes = models.TextField(blank=True, null=True)

    #TODO: This could be updated in a way that doesn't return the sample id in the admin panel.
    # It's confusing in the admin panel to see "Sample 3 from Thing1" when it's the first sample
    # from Thing1 but the third sample in the sample table. If this doesn't makes sense, try
    # creating three samples from two different Things from the admin panel.
    def __str__(self):
        return f"Sample {self.sample_id} from {self.thing}"


#--------Observation model-----------

class Observation(models.Model):
    """Represents a single observation from a datastream?"""
    observation_id = models.BigAutoField(primary_key=True)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name="observations", verbose_name="related sample")
    datastream = models.ForeignKey(Datastream, on_delete=models.CASCADE, related_name="observations", verbose_name="related datastream")
    observed_value = models.FloatField(help_text="The value of the observation")
    release_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Observation {self.observation_id} for {self.datastream}"

#--------GroundwaterLevelObservation model-----------
class GroundwaterLevelObservation(Observation):
    """A specific type of observation (groundwater levels)"""
    groundwater_level_observation_id = models.BigAutoField(primary_key=True)
    observation_ptr = models.OneToOneField(
        Observation,
        on_delete=models.CASCADE,
        parent_link=True,
        related_name='groundwater_level_observations',
        verbose_name="related observation"
    )

    def __str__(self):
        return f"Groundwater Level Observation {self.observation_id} for {self.datastream}"
