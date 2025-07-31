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