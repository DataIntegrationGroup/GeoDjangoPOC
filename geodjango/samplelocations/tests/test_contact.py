from django.test import TestCase
from ..models import Contact

class ContactModelTest(TestCase):
    def test_create_contact(self):
        contact = Contact.objects.create(name="John Doe", email="john@example.com", phone="1234567890")
        self.assertEqual(contact.name, "John Doe")
        self.assertEqual(contact.email, "john@example.com")
        self.assertEqual(contact.phone, "1234567890")
        self.assertIsNotNone(contact.date_created)

    def test_str_method(self):
        contact = Contact.objects.create(name="Jane Doe", email="jane@example.com")
        self.assertEqual(str(contact), "Jane Doe")

    def test_ordering(self):
        Contact.objects.create(name="B", email="b@example.com")
        Contact.objects.create(name="A", email="a@example.com")
        names = list(Contact.objects.values_list('name', flat=True))
        self.assertEqual(names, sorted(names))
