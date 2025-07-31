from samplelocations.tests import BaseTestClass
from samplelocations.models import Lexicon

class TestAddLexicon(BaseTestClass):
    """
    Test cases for adding lexicon categories and terms.
    """

    def setUp(self):
        super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_add_lexicon_category(self):
        name = "Test Category"
        description = "This is a test category."

        response = self.client.post(
            "/lexicon/category/add",
            json={"name": name, "description": description},
        )

        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["name"], name)
        self.assertEqual(data["description"], description)


    def test_add_lexicon_term(self):
        term = "test_term"
        definition = "This is a test definition."
        category = "Test Category"

        response = self.client.post(
            "/lexicon/add",
            json={"term": term, "definition": definition, "category": category},
        )

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["term"], term)
        self.assertEqual(data["definition"], definition)

    def test_add_triple(self):
        subject = {
            "term": "MG-030",
            "definition": "magdalena well",
            "category": "location_identifier",
        }
        predicate = "same_as"
        object_ = {
            "term": "USGS1234",
            "definition": "magdalena well",
            "category": "location_identifier",
        }

        response = self.client.post(
            "/lexicon/triple/add",
            json={
                "subject": subject,
                "predicate": predicate,
                "object_": object_,
            },
        )

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["subject"], subject["term"])
        self.assertEqual(data["predicate"], predicate)
        self.assertEqual(data["object_"], object_["term"])

class TestGetLexicon(BaseTestClass):

    def setUp(self):
        super().setUp()
        # Create a test category
        self.category = Lexicon.objects.create(
            name="Test Category",
            description="A category for testing",
        )

    def tearDown(self):
        return super().tearDown()

    def test_get_category(self):
        response = self.client.get(f"/lexicon/category/{self.category.name}")
        self.assertEqual(response.status_code, 200)