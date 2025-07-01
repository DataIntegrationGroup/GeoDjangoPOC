from django.test import TestCase
from ..models import Well, WellScreen, SampleLocation, Owner, Contact, Lexicon
from django.contrib.gis.geos import Point

class WellScreenModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(name="Contact", email="contact@example.com")
        self.owner = Owner.objects.create(name="Owner", contact=self.contact)
        self.location = SampleLocation.objects.create(name="Loc", point=Point(-105, 40), owner=self.owner)
        self.well = Well.objects.create(location=self.location)
        self.screen_type = Lexicon.objects.create(name="ScreenType1")

    def test_create_well_screen(self):
        screen = WellScreen.objects.create(
            well=self.well,
            screen_depth_top=10.0,
            screen_depth_bottom=20.0,
            screen_type=self.screen_type
        )
        self.assertEqual(screen.well, self.well)
        self.assertEqual(screen.screen_depth_top, 10.0)
        self.assertEqual(screen.screen_depth_bottom, 20.0)
        self.assertEqual(screen.screen_type, self.screen_type)

    def test_str_method(self):
        screen = WellScreen.objects.create(well=self.well, screen_depth_top=5.0, screen_depth_bottom=15.0)
        self.assertIn("5.0-15.0", str(screen))
        self.assertIn(str(self.well), str(screen))

# test comment
