"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

# from unittest import TestCase, main
from django.test import TestCase
from foodsite.library.models import Chef, Recipe, Region
from django.test import Client
import requests
import foodsite.library.views as V
# import coverage


class FoodsiteTest(TestCase):
    ##Model tests
    def setUp(self):
        japan = Region()
        japan.name = 'Japan'
        japan.image = 'x'
        japan.description = "x"
        japan.google_map = 'x'
        japan.save()
        s_usa = Region()
        s_usa.name = 'Southern USA'
        s_usa.image = "x"
        s_usa.description = "x"
        s_usa.google_map = "x"
        s_usa.save()
        g_brit = Region()
        g_brit.name = "Great Britain"
        g_brit.image = "x"
        g_brit.description = "x"
        g_brit.google_map = "x"
        g_brit.save()
        paula = Chef()
        paula.name = 'Paula Deen'
        paula.image = "x"
        paula.birth_place = "x"
        paula.birth_date = "1947-01-19"
        paula.region = Region.objects.get(name = "Southern USA")
        paula.style = "x"
        paula.youtube = "x"
        paula.twitter_link = "x"
        paula.twitter_id = "x"
        paula.bio = "x"
        paula.save()
        gordon = Chef()
        gordon.name = 'Gordon Ramsay'
        gordon.image = "x"
        gordon.birth_place = "x"
        gordon.birth_date = "1966-01-19"
        gordon.region = Region.objects.get(name = "Great Britain")
        gordon.style = "x"
        gordon.youtube = "x"
        gordon.twitter_link = "x"
        gordon.twitter_id = "x"
        gordon.bio = "x"
        gordon.save()
        masa = Chef()
        masa.name = 'Masaharu Morimoto'
        masa.image = "x"
        masa.birth_place = "x"
        masa.birth_date = "1947-01-19"
        masa.region = Region.objects.get(name = "Japan")
        masa.style = "x"
        masa.youtube = "x"
        masa.twitter_link = "x"
        masa.twitter_id = "x"
        masa.bio = "x"
        masa.save()
        veg = Recipe()
        veg.name = "Vegetable Sushi"
        veg.image = "x"
        veg.region = Region.objects.get(name = "Japan")
        veg.chef = Chef.objects.get(name = "Masaharu Morimoto")
        veg.ingredients = "x"
        veg.instructions = "x"
        veg.time_needed = "x"
        veg.difficulty = 'E'
        veg.dish_type = "x"
        veg.save()
        chicken = Recipe()
        chicken.name = "Southern Fried Chicken"
        chicken.image = "x"
        chicken.region = Region.objects.get(name = "Southern USA")
        chicken.chef = Chef.objects.get(name = "Paula Deen")
        chicken.ingredients = "x"
        chicken.instructions = "x"
        chicken.time_needed = "x"
        chicken.difficulty = 'E'
        chicken.dish_type = "x"
        chicken.save()
        pork = Recipe()
        pork.name = "Pork and Ham Pie"
        pork.image = "x"
        pork.region = Region.objects.get(name = "Great Britain")
        pork.chef = Chef.objects.get(name = "Gordon Ramsay")
        pork.ingredients = "x"
        pork.instructions = "x"
        pork.time_needed = "x"
        pork.difficulty = 'E'
        pork.dish_type = "x"
        pork.save()

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
        new_chef = Chef()
        new_chef.name = "British Chef"
        new_chef.region = great_britain
        new_chef.image = 'x'
        new_chef.birth_date = '2014-07-23'
        new_chef.birth_place = 'x'
        new_chef.style = 'x'
        new_chef.youtube = 'x'
        new_chef.twitter_link = 'x'
        new_chef.twitter_id = 'x'
        new_chef.bio = 'x'
        new_chef.save()
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
        new_recipe = Recipe()
        new_recipe.name = "Fried Stuff"
        new_recipe.chef = paula_deen
        new_recipe.image = 'x'
        new_recipe.region = Region.objects.get(name = 'Japan')
        new_recipe.ingredients = 'x'
        new_recipe.instructions = 'x'
        new_recipe.time_needed = 'x'
        new_recipe.difficulty = 'E'
        new_recipe.dish_type = 'x'
        new_recipe.save()
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
        new_recipe = Recipe()
        new_recipe.name = "Miso Soup"
        new_recipe.region = japan
        new_recipe.chef = Chef.objects.get(name = 'Masaharu Morimoto')
        new_recipe.image = 'x'
        new_recipe.ingredients = 'x'
        new_recipe.instructions = 'x'
        new_recipe.time_needed = 'x'
        new_recipe.difficulty = 'E'
        new_recipe.dish_type = 'x'
        new_recipe.save()
        japan_qset = Recipe.objects.filter(region__name = "Japan")
        try:
            some_recipe1 = japan_qset.get(name = "Miso Soup")
            some_recipe2 = japan_qset.get(name = "Vegetable Sushi")
        except Recipe.DoesNotExist:
            self.assertEqual(1, 0)
        self.assertEqual(some_recipe1, new_recipe)
        new_recipe.delete()


    ## API Tests ###

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

    def test_normalize_search_1(self):
        self.assertEqual(V.normalize_query('  some random  words "with   quotes  " and   spaces'), ['some', 'random', 'words', 'with quotes', 'and', 'spaces'])

    def test_normalize_search_2(self):
        self.assertEqual(V.normalize_query('  " " testing "stuf is cool"'), ['', 'testing', 'stuf is cool'])

    def test_normalize_search_3(self):
        self.assertEqual(V.normalize_query('                           '), [])

    def test_get_query_search_1(self):
        query_string = 'Gordon'
        chef_fields = ['bio', 'birth_date', 'birth_place', 'id', 'name', 'style', 'twitter_id']
        chef_query = V.get_query(query_string, chef_fields,True)
        chef_entries = Chef.objects.filter(chef_query)
        self.assertEqual(chef_entries[0].name, "Gordon Ramsay")

    def test_get_query_search_2(self):
        query_string = '"Ham Pie"'
        recipe_fields = ['name', 'ingredients', 'instructions', 'time_needed', 'difficulty', 'dish_type']
        recipe_query = V.get_query(query_string, recipe_fields,True)
        recipe_entries = Recipe.objects.filter(recipe_query)
        self.assertEqual(recipe_entries[0].name, "Pork and Ham Pie")

    def test_get_query_search_3(self):
        query_string = 'South'
        region_fields = ['name', 'description']
        region_query = V.get_query(query_string, region_fields,True)
        region_entries = Region.objects.filter(region_query)
        self.assertEqual(len(region_entries),1)
        self.assertEqual(region_entries[0].name, "Southern USA")

    def test_search_search_1(self):
        query_string = 'Gordon'
        self.assertEqual(V.search(q_string = query_string)["chefs"][0].name,"Gordon Ramsay")

    def test_search_search_2(self):
        query_string = '"Ham Pie"'
        self.assertEqual(V.search(q_string = query_string)["recipes"][0].name,"Pork and Ham Pie")

    def test_search_search_3(self):
        query_string = 'South'
        self.assertEqual(V.search(q_string = query_string)["regions"][0].name,"Southern USA")









# coverage.start()
# main()
# coverage.stop()
# coverage.report()
