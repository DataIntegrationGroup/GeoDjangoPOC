from samplelocations.tests import BaseTestClass
from samplelocations.models import Thing
from samplelocations.models import Location, Location_Thing_Junction
from pprint import pprint

class TestThing(BaseTestClass):
    """
    Test cases for the Thing model.
    """

    maxDiff = None

    def setUp(self):
        super().setUp()

        # Create Location records
        self.location1 = Location.objects.create(
            coordinate="POINT(10.0 10.0 100.0)",

        )
        self.location2 = Location.objects.create(
            coordinate="POINT(20.0 20.0 200.0)",
        )

        # Create Thing records
        self.well_thing = Thing.objects.create(
            name="Test Well",
            thing_type="W",
            release_status=True,
            well_depth_ft=100.0,
            hole_depth_ft=120.0,
            casing_diameter_ft=10.0,
            casing_depth_ft=80.0,
            casing_description="PVC",
            construction_notes="Test well construction notes",
        )
        self.spring_thing = Thing.objects.create(
            name="Test Spring",
            thing_type="S",
            release_status=True,
            spring_type="thermal",
        )

        # Create Location_Thing_Junction records
        self.junction1 = Location_Thing_Junction.objects.create(
            location_id=self.location1,
            thing_id=self.well_thing,
            effective_start="2023-10-01T00:00:00Z",
            effective_end="2040-01-01T00:00:00Z",  # Assuming a future end date for the test
        )
        self.junction2 = Location_Thing_Junction.objects.create(
            location_id=self.location2,
            thing_id=self.spring_thing,
            effective_start="2023-10-01T00:00:00Z",
            effective_end="2040-01-01T00:00:00Z",  # Assuming a future end date for the test
        )

        # Assign locations using the ManyToManyField
        self.well_thing.location_id.set([self.location1])
        self.spring_thing.location_id.set([self.location2])

    def tearDown(self):
        self.junction1.delete()
        self.junction2.delete()
        self.well_thing.delete()
        self.spring_thing.delete()
        self.location1.delete()
        self.location2.delete()
        return super().tearDown()

    def test_get_all_things(self):
        """
        List all things in the database as a feature collection
        """
        response = self.client.get("/api/thing")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["features"]), 2)
        self.assertEqual(
            data,
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [10.0, 10.0, 100.0]
                        },
                        "properties": {
                            "thing_id": self.well_thing.thing_id,
                            "name": self.well_thing.name,
                            "thing_type": "Well",
                            "release_status": self.well_thing.release_status,
                            "date_created": self.well_thing.date_created.isoformat(),
                            "well_depth_ft": self.well_thing.well_depth_ft,
                            "hole_depth_ft": self.well_thing.hole_depth_ft,
                            "casing_diameter_ft": self.well_thing.casing_diameter_ft,
                            "casing_depth_ft": self.well_thing.casing_depth_ft,
                            "casing_description": self.well_thing.casing_description,
                            "construction_notes": self.well_thing.construction_notes,
                        }
                    },
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [20.0, 20.0, 200.0]
                        },
                        "properties": {
                            "thing_id": self.spring_thing.thing_id,
                            "name": self.spring_thing.name,
                            "thing_type": "Spring",
                            "release_status": self.spring_thing.release_status,
                            "date_created": self.spring_thing.date_created.isoformat(),
                            "spring_type": self.spring_thing.spring_type,
                        }
                    }
                ]
            }
        )

    def test_get_thing_by_id(self):
        """
        Retrieve a specific thing by its ID as a feature collection
        """
        thing_id = self.well_thing.thing_id
        response = self.client.get(f"/api/thing/{thing_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(
            data,
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [10.0, 10.0, 100.0]
                        },
                        "properties": {
                            "thing_id": self.well_thing.thing_id,
                            "name": self.well_thing.name,
                            "thing_type": "Well",
                            "release_status": self.well_thing.release_status,
                            "date_created": self.well_thing.date_created.isoformat(),
                            "well_depth_ft": self.well_thing.well_depth_ft,
                            "hole_depth_ft": self.well_thing.hole_depth_ft,
                            "casing_diameter_ft": self.well_thing.casing_diameter_ft,
                            "casing_depth_ft": self.well_thing.casing_depth_ft,
                            "casing_description": self.well_thing.casing_description,
                            "construction_notes": self.well_thing.construction_notes,
                        }
                    },
                ]
            }
        )

    def test_404_not_found(self):
        """
        Test that a 404 is returned for a non-existent thing ID
        """
        response = self.client.get("/api/thing/9999")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["detail"], "Thing with id 9999 not found")
