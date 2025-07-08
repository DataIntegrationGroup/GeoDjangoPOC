from django.test import TestCase
from ninja.testing import TestClient
from geodjango.api import api


class BaseTestClass(TestCase):
    """
    Base class for all test cases.
    This class can be used to set up common fixtures or configurations
    that are shared across multiple test cases. 
    It can also be used to define common methods that can be reused
    in all test cases.
    """

    client = TestClient(api)

class TestLocations(BaseTestClass):

    def test_get_locations(self):
        response = self.client.get("/api/locations")
        self.assertEqual(response.status_code, 200)

    def test_post_location(self):
        location = {
            "name": "Test Location",
            "point": "POINT(10.1 10.1)",
            "visible": True,
        }
        response = self.client.post("/api/locations", json=location)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json()["id"])


class TestWells(BaseTestClass):

    def test_get_wells(self):
        response = self.client.get("/api/wells")
        self.assertEqual(response.status_code, 200)

    def test_post_well(self):
        well = {
            "location_id": 1,
            "api_id": "1001-0001",
            "ose_pod_id": "RA-0001",
            "well_type": "Monitoring",
            "well_depth": 100.0,
            "hole_depth": 100.0,
            "casing_diameter": 10.0,
            "casing_depth": 20.0,
            "casing_description": "foo bar",
            "formation_zone": "San Andres",
            "construction_notes": "this is a test of notes",
        }
        response = self.client.post("/api/wells", json=well)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json()["id"])


    def test_post_well_screen(self):
        well_screen = {
            "well_id": 1,
            "screen_depth_top": 100.0,
            "screen_depth_bottom": 120.0,
            "screen_type": "PVC",
        }
        response = self.client.post("/api/wells/well-screens/", json=well_screen)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json()["id"])


class TestContacts(BaseTestClass):

    def test_post_contact(self):
        contact = {
            "well_id": 1,
            "name": "John Doe",
            "email": "foo@gmail.com",
        }
        response = self.client.post("/api/wells/contacts/", json=contact)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json()["id"])

# #  ============== optional ? =============
# def test_add_lexicon():
#     formation = {
#         "term": "San Andres",
#         "definition": "Some sandstone unit",
#         "category": "Formations",
#     }

#     unit = {
#         "term": "TDS",
#         "definition": "Total Dissolved Solids",
#         "category": "water_chemistry",
#     }


# def test_add_lexicon_triple():
#     subject = {
#         "term": "MG-030",
#         "definition": "magdalena well",
#         "category": "location_identifier",
#     }
#     predicate = "same_as"
#     object_ = {
#         "term": "USGS1234",
#         "definition": "magdalena well",
#         "category": "location_identifier",
#     }


# def test_add_lexicon_triple_existing_subject():
#     subject = "TDS"
#     predicate = "same_as"
#     object_ = {
#         "term": "Total Dissolved Solids",
#         "definition": "all the solids dissolved in sample",
#         "category": "water_chemistry",
#     }


# def test_add_lexicon_triple_existing():
#     subject = "TDS"
#     predicate = "same_as"
#     object_ = "Total Dissolved Solids"


# ============= EOF =============================================