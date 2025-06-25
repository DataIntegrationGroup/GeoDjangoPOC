from django.contrib.gis.db import models

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