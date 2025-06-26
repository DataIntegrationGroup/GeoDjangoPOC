from django.contrib.gis.db import models

#-------- Lexicon model -----------
class Lexicon(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Lexicon"
        verbose_name_plural = "Lexicons"
        ordering = ['name']

#--------Sample Location base models -----------        

class SampleLocation(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    visible = models.BooleanField(default=False)
    point = models.PointField(srid=4326, spatial_index=True)
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('Owner', related_name='samplelocations', on_delete=models.CASCADE)
    #each sample location should have one owner, but an owner can have multiple sample locations
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Sample Location"
        verbose_name_plural = "Sample Locations"
        ordering = ['name']  # Order by name by default

class Owner(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    contact = models.ForeignKey('Contact', related_name='owners', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Owner"
        verbose_name_plural = "Owners"
        ordering = ['name']

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ['name']

class Well(models.Model):
    location = models.ForeignKey(SampleLocation, related_name='wells', on_delete=models.CASCADE)
    ose_pod_id = models.CharField(max_length=50, blank=True, null=True)
    api_id = models.CharField(max_length=50, blank=True, default="")
    usgs_id = models.CharField(max_length=50, blank=True, null=True)
    well_depth = models.FloatField(blank=True, null=True, help_text="feet below ground surface")
    hole_depth = models.FloatField(blank=True, null=True, help_text="feet below ground surface")
    well_type = models.ForeignKey(Lexicon, related_name='wells_by_type', on_delete=models.SET_NULL, blank=True, null=True)
    casing_diameter = models.FloatField(blank=True, null=True, help_text="inches")
    casing_depth = models.FloatField(blank=True, null=True, help_text="feet below ground surface")
    casing_description = models.CharField(max_length=50, blank=True, null=True)
    construction_notes = models.CharField(max_length=250, blank=True, null=True)
    formation_zone = models.ForeignKey(Lexicon, related_name='wells_by_formation', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"Well at {self.location.name}"

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