"""
def test_get_geojson():
    response = client.get("/location/feature_collection")
    assert response.status_code == 200
    data = response.json()
    assert "type" in data
    assert data["type"] == "FeatureCollection"
    assert "features" in data
    assert len(data["features"]) > 0  # Assuming there are features in the collection


def test_get_shapefile():
    response = client.get("/location/shapefile")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/zip"
    assert "Content-Disposition" in response.headers
    assert (
        'attachment; filename="locations.zip"'
        == response.headers["Content-Disposition"]
    )
"""

from samplelocations.tests import BaseTestClass
from samplelocations.models import Location

class TestAddLocation(BaseTestClass):

    def test_add_location_visible_is_true(self):
        response = self.client.post(
            "/location",
            json={
            "name": "Test Location 1",
            "point": "POINT(10.1 10.1)",
            "visible": True,
        },
    )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["id"], 2)

    def test_add_location_visible_is_false(self):
        response = self.client.post(
            "/location",
            json={
                "name": "Test Location 2",
            "point": "POINT(50.0 50.0)",
            "visible": False,
        },
    )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["id"], 3)


class TestGetLocation(BaseTestClass):

    def setUp(self):
        self.location = Location.objects.create(
            name="Test Location",
            point="POINT(10.0 10.0)",
            visible=True,
        )

    def tearDown(self):
        self.location.delete()
        return super().tearDown()

    def test_list_locations(self):
        """
        list al locations in the database as a feature collection
        """

    def get_specific_location(self):
        response = self.client.get(f"/location/{self.location.id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], self.location.id)
        self.assertEqual(data["name"], self.location.name)
        self.assertEqual(data["point"], "POINT(10.0 10.0)")

    def test_get_location_as_geojson(self):
        response = self.client.get("/location?format=feature-collection")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("type", data)
        self.assertEqual(data["type"], "FeatureCollection")
        self.assertIn("features", data)
        self.assertGreater(len(data["features"]), 0)  # Assuming there are features in the collection


    def test_get_location_as_shapefile(self):
        response = self.client.get("/location?format=shapefile")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/zip")
        self.assertIn("Content-Disposition", response.headers)
        self.assertEqual(
            'attachment; filename="locations.zip"',
            response.headers["Content-Disposition"]
        )