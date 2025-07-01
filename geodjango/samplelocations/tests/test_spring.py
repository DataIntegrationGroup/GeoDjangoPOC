from django.test import TestCase
from ..models import Spring, SampleLocation, Owner, Contact
from django.contrib.gis.geos import Point

class SpringModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(name="Contact", email="contact@example.com")
        self.owner = Owner.objects.create(name="Owner", contact=self.contact)
        self.location = SampleLocation.objects.create(name="Loc", point=Point(-105, 40), owner=self.owner)

    def test_create_spring(self):
        spring = Spring.objects.create(description="A spring", location=self.location)
        self.assertEqual(spring.description, "A spring")
        self.assertEqual(spring.location, self.location)

    def test_str_method(self):
        spring = Spring.objects.create(location=self.location)
        self.assertIn(self.location.name, str(spring))
