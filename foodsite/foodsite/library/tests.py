"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from unittest import TestCase, main
from foodsite.library.models import Chef, Recipe, Region
from django.test import Client
import requests
# import coverage


class ModelsUnitTest(TestCase):
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
        qset = Recipe.objects.filter(name__icontains="chicken")
        self.assertEqual(qset.exists(), True)

    def test_exclude(self) :
        some_recipe = Recipe.objects.get(name = "Southern Fried Chicken")
        qset = Recipe.objects.all().exclude(name__icontains="chicken")
        qset2 = qset.filter(name = some_recipe.name)
        self.assertEqual(qset2.exists(), False)

    def test_incorrect_lookup(self):
        try :
            some_chef = Chef.objects.get(name = "Pork and Ham Pie")
            self.assertEqual(1, 0)
        except Chef.DoesNotExist :
            self.assertEqual(1, 1)

    def test_multi_field_filter (self):
        qset = Recipe.objects.filter(chef__birth_date__year="1966", name__icontains="pork")
        try:
            some_recipe = qset.get(name = "Pork and Ham Pie")
        except Recipe.DoesNotExist:
            self.assertEqual(1, 0)
        self.assertEqual(1, 1)

    def test_chef_region_relationship(self):
        great_britain = Region.objects.get(name = "Great Britain")
        new_chef = Chef.objects.create(name = "British Chef", region = great_britain, image = 'x', birth_date = '2014-07-23', birth_place = 'x', style = 'x', youtube = 'x', twitter_link = 'x', twitter_id = 'x', bio = 'x')
        british_qset = Chef.objects.filter(region__name = "Great Britain")
        try:
            some_chef1 = british_qset.get(name = "British Chef")
            some_chef2 = british_qset.get(name = "Gordon Ramsay")
        except Chef.DoesNotExist:
            self.assertEqual(1, 0)
        self.assertEqual(some_chef1, new_chef)
        new_chef.delete()

    def test_chef_recipe_relationship(self):
        paula_deen = Chef.objects.get(name = "Paula Deen")
        new_recipe = Recipe.objects.create(name = "Fried Stuff", chef = paula_deen, image = 'x', region = Region.objects.get(name = 'Korea'), ingredients = 'x', instructions = 'x', time_needed = 'x', difficulty = 'E', dish_type = 'x')
        deen_qset = Recipe.objects.filter(chef__name = "Paula Deen")
        try:
            some_recipe1 = deen_qset.get(name = "Fried Stuff")
            some_recipe2 = deen_qset.get(name = "Southern Fried Chicken")
        except Recipe.DoesNotExist:
            self.assertEqual(1, 0)
        self.assertEqual(some_recipe1, new_recipe)
        new_recipe.delete()

    def test_recipe_region_relationship(self):
        japan = Region.objects.get(name = "Japan")
        new_recipe = Recipe.objects.create(name = "Miso Soup", region = japan, chef = Chef.objects.get(name = 'Masaharu Morimoto'), image = 'x', ingredients = 'x', instructions = 'x', time_needed = 'x', difficulty = 'E', dish_type = 'x')
        japan_qset = Recipe.objects.filter(region__name = "Japan")
        try:
            some_recipe1 = japan_qset.get(name = "Miso Soup")
            some_recipe2 = japan_qset.get(name = "Vegetable Sushi")
        except Recipe.DoesNotExist:
            self.assertEqual(1, 0)
        self.assertEqual(some_recipe1, new_recipe)
        new_recipe.delete()

    def test_chef_api_1(self):
        r = requests.get('http://regionalfoods.pythonanywhere.com/api/chef/1/')
        self.assertEqual(r.status_code, 200)
        resp_dict = r.json();
        self.assertEqual(len(resp_dict), 1)
        resp_dict = resp_dict[0]
        self.assertEqual(resp_dict["fields"]["name"], "Wolfgang Puck")

    def test_chef_api_2(self):
        r = requests.get('http://regionalfoods.pythonanywhere.com/api/chef/')
        self.assertEqual(r.status_code, 200)
        resp_dict = r.json();
        self.assertEqual(len(resp_dict), 10)
        resp_dict = resp_dict[0]
        self.assertEqual(resp_dict["fields"]["name"], "Wolfgang Puck")

    def test_cref_api_3(self):
        r = requests.get('http://regionalfoods.pythonanywhere.com/api/chef/300/')
        self.assertEqual(r.status_code, 404)

    def test_region_api_1(self):
        r = requests.get('http://regionalfoods.pythonanywhere.com/api/region/2/')
        self.assertEqual(r.status_code, 200)
        resp_dict = r.json();
        self.assertEqual(len(resp_dict), 1)
        resp_dict = resp_dict[0]
        self.assertEqual(resp_dict["fields"]["name"], "Southern USA")

    def test_region_api_2(self):
        r = requests.get('http://regionalfoods.pythonanywhere.com/api/region/')
        self.assertEqual(r.status_code, 200)
        resp_dict = r.json();
        self.assertEqual(len(resp_dict), 10)
        resp_dict = resp_dict[1]
        self.assertEqual(resp_dict["fields"]["name"], "Southern USA")

    def test_region_api_3(self):
        r = requests.get('http://regionalfoods.pythonanywhere.com/api/region/300/')
        self.assertEqual(r.status_code, 404)

    def test_recipe_api_1(self):
        r = requests.get('http://regionalfoods.pythonanywhere.com/api/recipe/11/')
        self.assertEqual(r.status_code, 200)
        resp_dict = r.json();
        self.assertEqual(len(resp_dict), 1)
        resp_dict = resp_dict[0]
        self.assertEqual(resp_dict["fields"]["name"], "Sparkling White Kimchi")

    def test_recipe_api_2(self):
        r = requests.get('http://regionalfoods.pythonanywhere.com/api/recipe/')
        self.assertEqual(r.status_code, 200)
        resp_dict = r.json();
        self.assertEqual(len(resp_dict), 10)
        resp_dict = resp_dict[9]
        self.assertEqual(resp_dict["fields"]["name"], "Sparkling White Kimchi")

    def test_recipe_api_3(self):
        r = requests.get('http://regionalfoods.pythonanywhere.com/api/recipe/300/')
        self.assertEqual(r.status_code, 404)



# coverage.start()
main()
# coverage.stop()
# coverage.report()
