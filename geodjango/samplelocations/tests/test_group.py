from samplelocations.tests import BaseTestClass


class TestAddGroup(BaseTestClass):

    def setUp(self):
        super().setUp()
        # Create a Thing instance for use in each test
        self.thing = self.Thing.objects.create(
            name="Test Thing",
            description="A thing for testing",
        )

    def tearDown(self):
        return super().tearDown()

    def test_add_group(self):
        response = self.client.post(
            "/group",
            json={"name": "Test Group"},
        )
        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", data)
        self.assertEqual(data["name"], "Test Group")


    def test_add_group_thing(self):
        response = self.client.post(
            "/group/association",
            json={"group_id": 1, "thing_id": self.thing.id},
        )
        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", data)
        self.assertEqual(data["group_id"], 1)
        self.assertEqual(data["thing_id"], self.thing.id)


# GET tests ======================================================

class TestGetGroup(BaseTestClass):

    def setUp(self):
        super().setUp()
        # Create a Group instance for use in each test
        self.group = self.Group.objects.create(name="Test Group")

    def tearDown(self):
        return super().tearDown()
    
    def test_get_groups(self):
        response = self.client.get("/group")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreater(len(data), 0)  # Assuming there are groups in the database

    def test_get_group_by_id(self):
        response = self.client.get(f"/group/{self.group.id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], self.group.id)
        self.assertEqual(data["name"], self.group.name)

    def test_get_group_association(self):
        response = self.client.get(f"/group/association/{self.group.id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreater(len(data), 0)