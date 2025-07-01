from django.test import TestCase
from ..models import Equipment, SampleLocation, Owner, Contact
from django.contrib.gis.geos import Point
from datetime import datetime

class EquipmentModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(name="Contact", email="contact@example.com")
        self.owner = Owner.objects.create(name="Owner", contact=self.contact)
        self.location = SampleLocation.objects.create(name="Loc", point=Point(-105, 40), owner=self.owner)

    def test_create_equipment(self):
        eq = Equipment.objects.create(
            equipment_type="Pump",
            model="ModelX",
            serial_no="SN123",
            date_installed=datetime(2020, 1, 1),
            date_removed=datetime(2021, 1, 1),
            recording_interval=60,
            equipment_notes="Test notes",
            location=self.location
        )
        self.assertEqual(eq.equipment_type, "Pump")
        self.assertEqual(eq.model, "ModelX")
        self.assertEqual(eq.serial_no, "SN123")
        self.assertEqual(eq.date_installed.year, 2020)
        self.assertEqual(eq.date_removed.year, 2021)
        self.assertEqual(eq.recording_interval, 60)
        self.assertEqual(eq.equipment_notes, "Test notes")
        self.assertEqual(eq.location, self.location)

    def test_str_method(self):
        eq = Equipment.objects.create(equipment_type="Sensor", model="M1", serial_no="S1", location=self.location)
        self.assertIn("Sensor", str(eq))
        self.assertIn(self.location.name, str(eq))
