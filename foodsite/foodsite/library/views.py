from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core import serializers
from foodsite.library.models import Chef, Recipe, Region
from itertools import chain

import requests
import re

from django.db.models import Q

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields, isAND):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        elif isAND:
            query = query & or_query
        else:
            query = query | or_query
    return query

def search(request=None, q_string=''):
    context = RequestContext(request)
    query_string = ''
    #found_entries = None
    context_dict = {}
    if request is None and q_string == '':
        return
    if  (q_string != '') or (('q' in request.GET) and request.GET['q'].strip()):
        if request is not None:
            query_string = request.GET['q']
        else:
            query_string = q_string

        # query_string_list = str.split(query_string)

        chef_fields = ['bio', 'birth_date', 'birth_place', 'id', 'name', 'style', 'twitter_id']
        recipe_fields = ['name', 'ingredients', 'instructions', 'time_needed', 'difficulty', 'dish_type']
        region_fields = ['name', 'description']

        chef_query = get_query(query_string, chef_fields, True)
        recipe_query = get_query(query_string, recipe_fields, True)
        region_query = get_query(query_string, region_fields, True)

        chef_entries = Chef.objects.filter(chef_query)
        recipe_entries = Recipe.objects.filter(recipe_query)
        region_entries = Region.objects.filter(region_query)

        ## Trying OR stuff here
        or_chef_query = get_query(query_string, chef_fields, False)
        or_recipe_query = get_query(query_string, recipe_fields, False)
        or_region_query = get_query(query_string, region_fields, False)

        or_chef_entries = Chef.objects.filter(or_chef_query)
        or_recipe_entries = Recipe.objects.filter(or_recipe_query)
        or_region_entries = Region.objects.filter(or_region_query)

        # for s in query_string_list:
        #     or_chef_query = get_query(s, chef_fields)
        #     or_recipe_query = get_query(s, recipe_fields)
        #     or_region_query = get_query(s, region_fields)

        #     or_chef_entries = set(chain(or_chef_entries, Chef.objects.filter(or_chef_query)))
        #     or_recipe_entries = set(chain(or_recipe_entries, Recipe.objects.filter(or_recipe_query)))
        #     or_region_entries = set(chain(or_region_entries, Region.objects.filter(or_region_query)))

        #found_entries = list(chain(chef_entries, recipe_entries, region_entries))

        # or_recipe_entries = or_recipe_entries.distinct()

        context_dict = {'query_string': query_string, 'chefs': chef_entries, 'regions': region_entries, 'recipes': recipe_entries, \
                        'or_chefs': or_chef_entries, 'or_regions': or_region_entries, 'or_recipes': or_recipe_entries}
    if request is None:
        return context_dict

    return render_to_response('search_result.html', context_dict,context)

# def search2(request, s):
#     entry_query = get_query(s,['id','name'])
#     found_entry = Chef.objects.filter(entry_query)
#     return render_to_response('search_result.html', {'string': s, 'entries': found_entry},context_instance=RequestContext(request))


# def query(response):
#     params = response.GET.get('q', '')
#     link = [];
#     link.append(chef_url(response,params))
#     # link.append(recipe_url(response,params))
#     # link.append(region_url(response,params))
#     #linkappend
#     return link

# def chef_url(response, params):
#     chefs = Chef.objects
#     items = chef.all()

#     return 0


def get_chef(request, chef_pk):
    chef_pk = str(chef_pk)
    chefs = Chef.objects
    if (chef_pk == "None"):
        items = chefs.all()
    elif chefs.filter(pk=chef_pk):
        items = chefs.filter(pk=chef_pk)
    else:
        raise Http404
    items = serializers.serialize('json', items, indent=0)
    return HttpResponse(items, content_type='application/json')

def get_region(request, region_pk):
    region_pk = str(region_pk)
    regions = Region.objects
    if (region_pk == "None"):
        items = regions.all()
    elif (regions.filter(pk=region_pk)):
        items = regions.filter(pk=region_pk)
    else:
        raise Http404
    items = serializers.serialize('json', items, indent=0)
    return HttpResponse(items, content_type='application/json')

def get_recipe(request, recipe_pk):
    recipe_pk = str(recipe_pk)
    recipes = Recipe.objects
    if (recipe_pk == "None"):
        items = recipes.all()
    elif (recipes.filter(pk=recipe_pk)):
        items = recipes.filter(pk=recipe_pk)
    else:
        raise Http404
    items = serializers.serialize('json', items, indent=0)
    return HttpResponse(items, content_type='application/json')


def chef(request, chef_name_url):
    # Request our context from the request passed to us.
    context = RequestContext(request)

    # Change underscores in the category name to spaces.
    # URLs don't handle spaces well, so we encode them as underscores.
    # We can then simply replace the underscores with spaces again to get the name.
    chef_name = chef_name_url.replace('_', ' ')

    # Create a context dictionary which we can pass to the template rendering engine.
    # We start by containing the name of the category passed by the user.
    context_dict = {'chef_name': chef_name}

    try:
        # Can we find a category with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        chef = Chef.objects.get(name=chef_name)

        # # Retrieve all of the associated pages.
        # # Note that filter returns >= 1 model instance.
        recipes = Recipe.objects.filter(chef = chef)

        # Adds our results list to the template context under name pages.
        context_dict['recipes'] = recipes
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['chef'] = chef
    except Chef.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render_to_response('chef.html', context_dict, context)

def recipe(request, recipe_name_url):

    context = RequestContext(request)
    recipe_name = recipe_name_url.replace('_', ' ')
    context_dict = {'recipe_name': recipe_name}

    try:
        recipe = Recipe.objects.get(name=recipe_name)
        context_dict['recipe'] = recipe
    except Recipe.DoesNotExist:
        pass


    # Go render the response and return it to the client.
    return render_to_response('recipe.html', context_dict, context)

def region(request, region_name_url):

    context = RequestContext(request)
    region_name = region_name_url.replace('_', ' ')
    context_dict = {'region_name': region_name}

    try:
        region = Region.objects.get(name=region_name)
        recipes = Recipe.objects.filter(region = region)
        for recipe in recipes:
            recipe_name = recipe.name.replace(' ', '_')
        chefs = Chef.objects.filter(region = region)
        context_dict['recipes'] = recipes
        context_dict['chefs'] = chefs
        context_dict['region'] = region
    except Region.DoesNotExist:
        pass


    # Go render the response and return it to the client.
    return render_to_response('region.html', context_dict, context)

def chefmain(request):

    context = RequestContext(request)
    chef_list = Chef.objects.all()
    context_dict = {'chefs': chef_list}

    for chef in chef_list:
        chef.url = chef.name.replace(' ', '_')
    return render_to_response('chefmain.html', context_dict, context)

def recipemain(request):

    context = RequestContext(request)
    recipe_list = Recipe.objects.all()
    context_dict = {'recipes': recipe_list}

    for recipe in recipe_list:
        recipe.url = recipe.name.replace(' ', '_')

    # recipe_list_mod = []
    # recipes_iter = iter(recipe_list)
    # while True:
    #     new_list = []
    #     try:
    #         for i in range(4):
    #             new_list.append(next(recipes_iter))
    #         recipe_list_mod.append(new_list)
    #     except StopIteration:
    #         recipe_list_mod.append(new_list)
    #         break
    # context_dict['recipes_mod'] = recipe_list_mod

    return render_to_response('recipemain.html', context_dict, context)

def regionmain(request):

    context = RequestContext(request)
    region_list = Region.objects.all()
    context_dict = {'regions': region_list}

    for region in region_list:
        region.url = region.name.replace(' ', '_')
    return render_to_response('regionmain.html', context_dict, context)

def sochimain(request):
    context = RequestContext(request)
    region_list = Region.objects.all()
    r = requests.get('http://ajhooper.pythonanywhere.com/api/country/?format=json')
    r = r.json()
    r2 = requests.get('http://ajhooper.pythonanywhere.com/api/athlete/?format=json')
    r2 = r2.json()

    # matching_list = []
    # for a in region_list:
    #     for b in r:
    #         if (str(a) == b["name"]):
    #             matching_list += b
    # context_dict = {'regions': matching_list}

    context_dict = { 'countries' : r}
    context_dict['regions'] = region_list
    context_dict['athletes'] = r2


    return render_to_response('olympicad.html', context_dict, context)
