"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
import foodsite.library.models as mods

class RegionTest(TestCase):
    def setUp(self):
        region = mods.Region()
        region.name = 'Middle Earth'
        region.description = "Middle-earth is the fictional universe setting of the majority of author J. R. R. Tolkien's fantasy writings"
        region.example_dishes = "Farmer Maggot's mushrooms, Potato stew, Lembas"
        region.save()

    def test_create_region(self):
        all_regions = mods.Region.objects.all()
        self.assertEqual(len(all_regions), 1)
        region = mods.Region.objects.first()