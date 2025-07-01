from django.test import TestCase
from django.contrib.gis.geos import Point
from ..models import SampleLocation, Owner, Contact

class SampleLocationModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(name="Contact", email="contact@example.com")
        self.owner = Owner.objects.create(name="Owner", contact=self.contact)

    def test_create_sample_location(self):
        point = Point(-105.0, 40.0)
        loc = SampleLocation.objects.create(
            name="Loc1",
            description="Test location",
            visible=True,
            point=point,
            owner=self.owner
        )
        self.assertEqual(loc.name, "Loc1")
        self.assertEqual(loc.description, "Test location")
        self.assertTrue(loc.visible)
        self.assertEqual(loc.point, point)
        self.assertEqual(loc.owner, self.owner)
        self.assertIsNotNone(loc.date_created)

    def test_str_method(self):
        point = Point(-105.0, 40.0)
        loc = SampleLocation.objects.create(name="Loc2", point=point, owner=self.owner)
        self.assertEqual(str(loc), "Loc2")

    def test_ordering(self):
        point = Point(-105.0, 40.0)
        SampleLocation.objects.create(name="B", point=point, owner=self.owner)
        SampleLocation.objects.create(name="A", point=point, owner=self.owner)
        names = list(SampleLocation.objects.values_list('name', flat=True))
        self.assertEqual(names, sorted(names))
