from django.test import TestCase
from ..models import Lexicon

class LexiconModelTest(TestCase):
    def test_create_lexicon(self):
        lex = Lexicon.objects.create(name="Test Lexicon", description="A test lexicon.")
        self.assertEqual(lex.name, "Test Lexicon")
        self.assertEqual(lex.description, "A test lexicon.")
        self.assertIsNotNone(lex.date_created)

    def test_str_method(self):
        lex = Lexicon.objects.create(name="Lexicon1")
        self.assertEqual(str(lex), "Lexicon1")

    def test_ordering(self):
        Lexicon.objects.create(name="B")
        Lexicon.objects.create(name="A")
        names = list(Lexicon.objects.values_list('name', flat=True))
        self.assertEqual(names, sorted(names))
