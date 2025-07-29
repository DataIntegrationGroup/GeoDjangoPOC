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

# class TestAddLocation(BaseTestClass):

#     def test_add_location_visible_is_true(self):
#         response = self.client.post(
#             "/location",
#             json={
#             "name": "Test Location 1",
#             "point": "POINT(10.1 10.1)",
#             "visible": True,
#         },
#     )
#         self.assertEqual(response.status_code, 201)
#         data = response.json()
#         self.assertEqual(data["id"], 2)

#     def test_add_location_visible_is_false(self):
#         response = self.client.post(
#             "/location",
#             json={
#                 "name": "Test Location 2",
#             "point": "POINT(50.0 50.0)",
#             "visible": False,
#         },
#     )
#         self.assertEqual(response.status_code, 201)
#         data = response.json()
#         self.assertEqual(data["id"], 3)


class TestGetLocation(BaseTestClass):

    def setUp(self):
        self.location_1 = Location.objects.create(
            coordinate = "POINT(10 10 100)"
        )

        self.location_2 = Location.objects.create(
            coordinate = "POINT(20 20 200)",
        )

    def tearDown(self):
        self.location_1.delete()
        self.location_2.delete()
        return super().tearDown()

    def test_get_all_locations(self):
        """
        Tests that all locations can be listed
        """
        response = self.client.get("/api/location")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["coordinates"], f"POINT({self.location_1.coordinate.x} {self.location_1.coordinate.y} {self.location_1.coordinate.z})")
        self.assertEqual(data[1]["coordinates"], f"POINT({self.location_2.coordinate.x} {self.location_2.coordinate.y} {self.location_2.coordinate.z})")

    def test_get_location_by_id(self):
        """
        Tests that a specific location can be retrieved by its ID
        """
        self.maxDiff = None
        response = self.client.get(f"/api/location/{self.location_1.location_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(
            data,
            {
                "location_id": self.location_1.location_id,
                "coordinates": f"POINT({self.location_1.coordinate.x} {self.location_1.coordinate.y} {self.location_1.coordinate.z})",
                "date_created": self.location_1.date_created.isoformat(),
            }
        )

    def test_404_location_not_found(self):
        """
        Tests that a 404 is returned when trying to access a non-existent location
        """
        response = self.client.get("/api/location/9999")
        print(response)
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertEqual(data["detail"], "Location with location_id 9999 not found")