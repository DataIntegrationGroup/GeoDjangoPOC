from samplelocations.tests import BaseTestClass
from samplelocations.models import Thing

class TestThing(BaseTestClass):
    """
    Test cases for the Thing model.
    """

    def setUp(self):
        super().setUp()
        # Create a Thing instance for use in each test
        self.thing = Thing.objects.create(
            name="Test Thing",
            description="A thing for testing",
        )

    def tearDown(self):
        self.thing.delete()
        return super().tearDown()

    def test_get_all_things(self):
        """
        List all things in the database as a feature collection
        """
        pass

    def test_get_thing_by_id(self):
        """
        Retrieve a specific thing by its ID as a feature collection
        """