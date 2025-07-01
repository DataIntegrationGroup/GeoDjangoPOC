from django.test import TestCase
from ..models import Well, SampleLocation, Owner, Contact, Lexicon
from django.contrib.gis.geos import Point

class WellModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(name="Contact", email="contact@example.com")
        self.owner = Owner.objects.create(name="Owner", contact=self.contact)
        self.location = SampleLocation.objects.create(name="Loc", point=Point(-105, 40), owner=self.owner)
        self.lexicon = Lexicon.objects.create(name="Type1")
        self.formation = Lexicon.objects.create(name="Formation1")

    def test_create_well(self):
        well = Well.objects.create(
            location=self.location,
            ose_pod_id="POD123",
            api_id="API123",
            usgs_id="USGS123",
            well_depth=100.0,
            hole_depth=110.0,
            well_type=self.lexicon,
            casing_diameter=6.0,
            casing_depth=80.0,
            casing_description="Steel",
            construction_notes="Notes",
            formation_zone=self.formation
        )
        self.assertEqual(well.location, self.location)
        self.assertEqual(well.ose_pod_id, "POD123")
        self.assertEqual(well.api_id, "API123")
        self.assertEqual(well.usgs_id, "USGS123")
        self.assertEqual(well.well_depth, 100.0)
        self.assertEqual(well.hole_depth, 110.0)
        self.assertEqual(well.well_type, self.lexicon)
        self.assertEqual(well.casing_diameter, 6.0)
        self.assertEqual(well.casing_depth, 80.0)
        self.assertEqual(well.casing_description, "Steel")
        self.assertEqual(well.construction_notes, "Notes")
        self.assertEqual(well.formation_zone, self.formation)

    def test_str_method(self):
        well = Well.objects.create(location=self.location)
        self.assertIn(self.location.name, str(well))

