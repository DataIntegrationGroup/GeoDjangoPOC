# hello
# This file is now split into test_contact.py and test_owner.py. You can remove this file if you wish.

from django.test import TestCase
from ..models import Contact, Owner


class OwnerModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(name="Owner Contact", email="owner@example.com")

    def test_create_owner(self):
        owner = Owner.objects.create(name="Owner1", contact=self.contact)
        self.assertEqual(owner.name, "Owner1")
        self.assertEqual(owner.contact, self.contact)
        self.assertIsNotNone(owner.date_created)

    def test_str_method(self):
        owner = Owner.objects.create(name="Owner2", contact=self.contact)
        self.assertEqual(str(owner), "Owner2")

    def test_ordering(self):
        Owner.objects.create(name="B", contact=self.contact)
        Owner.objects.create(name="A", contact=self.contact)
        names = list(Owner.objects.values_list('name', flat=True))
        self.assertEqual(names, sorted(names))
