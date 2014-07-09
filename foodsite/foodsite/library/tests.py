"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from foodsite.library.models import Region, Chef, Recipe

class UnitTest(TestCase):
    def test_str_region(self) :
        reg = Region.objects.get(name = "Japan")
        self.assertEqual(str(reg), "Japan")

    def test_str_chef(self) :
        ch = Chef.objects.get(name = "Gordon Ramsay")
        self.assertEqual(str(ch), "Gordon Ramsay")

    def test_str_recipe(self) :
        rec = Recipe.objects.get(name = "Southern Fried Chicken")
        self.assertEqual(str(rec), "Southern Fried Chicken")

    def test_foreign_key(self) :
        reg = Region.objects.get(name = "Southern USA")
        rec = Recipe.objects.get(region = reg)
        self.assertEqual(rec.name, "Southern Fried Chicken")