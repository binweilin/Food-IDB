"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from foodsite.library.models import Region, Chef, Recipe

class UnitTest(TestCase):
    def test_str_region(self):
        some_region = Region.objects.get(name = "Japan")
        self.assertEqual(str(some_region), "Japan")

    def test_str_chef(self):
        some_chef = Chef.objects.get(name = "Gordon Ramsay")
        self.assertEqual(str(some_chef), "Gordon Ramsay")

    def test_str_recipe(self):
        some_recipe = Recipe.objects.get(name = "Southern Fried Chicken")
        self.assertEqual(str(some_recipe), "Southern Fried Chicken")

    def test_foreign_key(self):
        some_region = Region.objects.get(name = "Southern USA")
        some_recipe = Recipe.objects.get(region = some_region)
        self.assertEqual(some_recipe.name, "Southern Fried Chicken")

    def test_filter_contains(self):
        some_entree = Recipe.objects.get(name = "Southern Fried Chicken")
        qset = Recipe.objects.all().filter(name = some_entree.name)
        self.assertEqual(qset.exists(), True)

    def test_field_contains(self):
        qset = Recipe.objects.get(name__icontains="chicken")
        self.assertEqual(qset.exists(), True)

    def test_exclude(self) :
        some_recipe = Recipe.objects.get(name = "Southern Fried Chicken")
        qset = Recipe.objects.all().exclude(name__icontains="chicken")
        qset2 = qset.filter(name = some_recipe.name)
        self.assertEqual(qset2.exists(), False)

    def test_incorrect_lookup(self):
        try :
            some_chef = Chef.objects.get(name = "Pork and Ham Pie")
        except Chef.DoesNotExist :
            self.assertEqual(1, 1)
        self.assertEqual(1, 0)

    def test_multi_field_filter (self):
        qset = Recipe.objects.filter(chef__birth_date__year="1966", name__icontains="pork")
        try:
            some_recipe = qset.get(name = "Pork and Ham Pie")
        except Recipe.DoesNotExist:
            self.assertEqual(1, 0)
        self.assertEqual(1, 1)

    def test_chef_region_relationship(self):
        great_britain = Region.objects.get(name = "Great Britain")
        new_chef = Chef.objects.create(name = "British Chef", region = great_britain)
        british_qset = Chef.objects.filter(region__name = "Great Britain")
        try:
            some_chef1 = british.qset.get(name = "British Chef")
            some_chef2 = british_qset.get(name = "Gordon Ramsay")
        except Chef.DoesNotExist:
            self.assertEqual(1, 0)
        self.assertEqual(some_chef1, new_chef)
        new_chef.delete()

    def test_chef_recipe_relationship(self):
        paula_deen = Chef.objects.get(name = "Paula Deen")
        new_recipe = Recipe.objects.create(name = "Fried Stuff", chef = paula_deen)
        deen_qset = Recipe.objects.filter(chef__name = "Paula Deen")
        try:
            some_recipe1 = deen.qset.get(name = "Fried Stuff")
            some_recipe2 = deen_qset.get(name = "Southern Fried Chicken")
        except Recipe.DoesNotExist:
            self.assertEqual(1, 0)
        self.assertEqual(some_recipe1, new_recipe)
        new_recipe.delete()

    def test_recipe_region_relationship(self):
        japan = Region.objects.get(name = "Japan")
        new_recipe = Recipe.objects.create(name = "Miso Soup", region = japan)
        japan_qset = Chef.objects.filter(region__name = "Japan")
        try:
            some_recipe1 = japan_qset.get(name = "Miso Soup")
            some_recipe2 = japan.qset.get(name = "Vegetable Sushi")
        except Recipe.DoesNotExist:
            self.assertEqual(1, 0)
        self.assertEqual(some_recipe1, new_recipe)
        new_recipe.delete()


