from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from samplelocations.models import (
    Lexicon, SampleLocation, Owner, Contact, Well, WellScreen, Equipment, Spring
)
import random

class Command(BaseCommand):
    help = "Seed the database with sample data for all models"

    def handle(self, *args, **kwargs):

        well_types = ['Production', 'Observation']
        formation_zones = ['Sandstone', 'Limestone']
        screen_types = ['PVC', 'Steel']

        lexicon_terms = []
        for term in well_types + formation_zones + screen_types:
            lexicon_terms.append(Lexicon.objects.create(name=term, description=f"{term} type"))

        contacts = []
        for i in range(3):
            contacts.append(Contact.objects.create(
                name=f"Contact {i+1}",
                email=f"contact{i+1}@example.com",
                phone=f"555-000{i+1}"
            ))

        owners = []
        for i in range(3):
            owners.append(Owner.objects.create(
                name=f"Owner {i+1}",
                description=f"Description for Owner {i+1}",
                contact=random.choice(contacts)
            ))

        # Seed 8 SampleLocations as Wells
        locations = []
        for i in range(8):
            loc = SampleLocation.objects.create(
                name=f"Well Location {i+1}",
                description=f"Description for Well Location {i+1}",
                visible=True,
                point=Point(
                    random.uniform(-106, -107),  
                    random.uniform(32, 38),     
                    srid=4326
                ),
                owner=random.choice(owners)
            )
            locations.append(loc)
            # Create Well for this location
            well = Well.objects.create(
                location=loc,
                ose_pod_id=f"OSE{i+1:03d}",
                api_id=f"API{i+1:03d}",
                usgs_id=f"USGS{i+1:03d}",
                well_depth=random.uniform(100, 500),
                hole_depth=random.uniform(100, 500),
                well_type=Lexicon.objects.filter(name__in=well_types).order_by('?').first(),
                casing_diameter=random.uniform(4, 12),
                casing_depth=random.uniform(50, 100),
                casing_description="Standard casing",
                construction_notes="Standard construction",
                formation_zone=Lexicon.objects.filter(name__in=formation_zones).order_by('?').first()
            )
            # Add screen
            WellScreen.objects.create(
                well=well,
                screen_depth_top=random.uniform(10, 50),
                screen_depth_bottom=random.uniform(51, 100),
                screen_type=Lexicon.objects.filter(name__in=screen_types).order_by('?').first()
            )
            # Add Equipment
            Equipment.objects.create(
                equipment_type="Pump",
                model="Model X",
                serial_no=f"SN{i+1:03d}",
                date_installed=None,
                date_removed=None,
                recording_interval=60,
                equipment_notes="Initial install",
                location=loc
            )

        # Seed 2 SampleLocations as Springs
        for i in range(2):
            loc = SampleLocation.objects.create(
                name=f"Spring Location {i+1}",
                description=f"Description for Spring Location {i+1}",
                visible=True,
                point=Point(
                    random.uniform(-125, -65),
                    random.uniform(25, 50),
                    srid=4326
                ),
                owner=random.choice(owners)
            )
            locations.append(loc)
            Spring.objects.create(
                description=f"Spring at {loc.name}",
                location=loc
            )

        self.stdout.write(self.style.SUCCESS("Seeded 8 wells and 2 springs with related models."))