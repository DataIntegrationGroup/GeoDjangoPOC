from . import BaseTestClass

#  ADD tests ======================================================


from geodjango.samplelocations.models import Thing

class TestAddContact(BaseTestClass):
    """
    Test cases for adding contacts.
    """

    def setUp(self):
        super().setUp()
        # Create a Thing instance for use in each test
        self.thing = Thing.objects.create(
            name="Test Thing",
            description="A thing for testing",
        )

    def tearDown(self):
        return super().tearDown()

    def test_add_contact(self):
        response = self.client.post(
            "/contact",
            json={
                "name": "Test Contact",
                "role": "Owner",
                "thing_id": self.thing.thing_id,
                "emails": [{"email": "test@example.com", "email_type": "Primary"}],
                "phones": [{"phone_number": "+12345678901", "phone_type": "Primary"}],
                "addresses": [
                    {
                        "address_line_1": "123 Main St",
                        "city": "Test City",
                        "state": "NM",
                        "postal_code": "87501",
                        "country": "US",
                        "address_type": "Primary",
                    }
                ],
            },
        )
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("id", data)
        self.assertEqual(data["name"], "Test Contact")
        self.assertEqual(data["role"], "Owner")

        self.assertEqual(len(data["emails"]), 1)
        self.assertEqual(data["emails"][0]["email"], "test@example.com")
        self.assertIn("id", data)
        self.assertEqual(data["name"], "Test Contact")
        self.assertEqual(data["role"], "Owner")

        self.assertEqual(len(data["emails"]), 1)
        self.assertEqual(data["emails"][0]["email"], "test@example.com")

        self.assertEqual(len(data["phones"]), 1)
        self.assertEqual(data["phones"][0]["phone_number"], "+12345678901")
        self.assertEqual(len(data["addresses"]), 1)
        self.assertEqual(data["addresses"][0]["address_line_1"], "123 Main St")


    def test_phone_validation_fail(self):
        for phone in [
            "definitely not a phone",
            # "1234567890",
            # "123-456-7890",
            # "123-456-78901",
            # "123-4567-890",
            "123-456-789a",
            "123-456-7890x1234",
            "123.456.7890",
            "(123) 456-7890",
        ]:

            response = self.client.post(
                "/contact",
                json={
                    "name": "Test Contact 2",
                    "thing_id": self.thing.thing_id,
                    "role": "Primary",
                    "emails": [{"email": "fasdfasdf@gmail.com", "email_type": "Primary"}],
                    "phones": [{"phone_number": phone, "phone_type": "Primary"}],
                    "addresses": [
                        {
                            "address_line_1": "123 Main St",
                            "city": "Test City",
                            "state": "NM",
                            "postal_code": "87501",
                            "country": "US",
                            "address_type": "Primary",
                        }
                    ],
                },
            )
            data = response.json()
            self.assertEqual(response.status_code, 422)
            self.assertIn("detail", data, "Expected 'detail' in response")
            self.assertEqual(len(data["detail"]), 1, "Expected 1 error in response")
            detail = data["detail"][0]
            self.assertEqual(detail["msg"], f"Value error, Invalid phone number. {phone}")


    def test_email_validation_fail(self):

        for email in [
            "",
            "invalid-email",
            "invalid@domain",
            "invalid@domain.",
            "@domain.com",
        ]:
            response = self.client.post(
                "/contact",
                json={
                    "name": "Test ContactX",
                    "thing_id": self.thing.thing_id,
                    "role": "Primary",
                    "emails": [{"email": email, "email_type": "Primary"}],
                    "phones": [{"phone_number": "+12345678901", "phone_type": "Primary"}],
                    "addresses": [
                        {
                            "address_line_1": "123 Main St",
                            "city": "Test City",
                            "state": "NM",
                            "postal_code": "87501",
                            "country": "US",
                            "address_type": "Primary",
                        }
                    ],
                },
            )
            data = response.json()
            self.assertEqual(response.status_code, 422)
            self.assertIn("detail", data, "Expected 'detail' in response")
            self.assertEqual(len(data["detail"]), 1, "Expected 1 error in response")
            detail = data["detail"][0]
            self.assertEqual(detail["msg"], f"Value error, Invalid email format. {email}")


# GET tests ======================================================

class TestGetContact(BaseTestClass):

    def test_get_contacts(self):
        response = self.client.get("/contact")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)

    def test_item_get_contact(self):
        response = self.client.get("/contact/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["name"], "Test Contact")