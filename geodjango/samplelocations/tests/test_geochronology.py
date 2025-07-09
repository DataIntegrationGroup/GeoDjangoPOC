from . import BaseTestClass
from geodjango.samplelocations.models import Thing, Location, Geochronology

class TestAddGeochronology(BaseTestClass):

    def setUp(self):
        super().setUp()
        # Create a Thing instance for use in each test
        self.thing = self.Thing.objects.create(name="Test Thing", description="A thing for testing")
        # Create a Location instance for use in each test
        self.location = Location.objects.create(name="Test Location", description="A location for testing")

    def tearDown(self):
        return super().tearDown()

    def test_add_age(self):

        response = self.client.post(
            "/geochronology",
            json={
                "location_id": self.location.location_id,
                "age": 100,
                "age_unit": "Ma",
                "thing_id": self.thing.thing_id,
            },
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", data)
        self.assertEqual(data["age"], 100)
        self.assertEqual(data["age_unit"], "Ma")