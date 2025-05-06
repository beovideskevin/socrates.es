from django.test import TestCase
from .models import Tag

# Create your tests here.
class Test(TestCase):
    def setUp(self):
        t = Tag.objects.create(name="Love")

    def test_tags_count(self):
        self.assertEquals(Tag.objects.count(), 1)
