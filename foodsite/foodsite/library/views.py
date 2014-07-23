from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from foodsite.library.models import Chef, Recipe, Region

def index2(request):
    #return HttpResponse("Rango says hello world!")
    context = RequestContext(request)
    chef_list = Chef.objects.all()
    context_dict = {'chefs': chef_list}
    recipe_list = Recipe.objects.all()
    context_dict = {'recipes': recipe_list}
    for chef in chef_list:
        chef.url = chef.name.replace(' ', '_')
    return render_to_response('index2.html', context_dict, context)


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
    return render_to_response('recipemain.html', context_dict, context)

def regionmain(request):

    context = RequestContext(request)
    region_list = Region.objects.all()
    context_dict = {'regions': region_list}

    for region in region_list:
        region.url = region.name.replace(' ', '_')
    return render_to_response('regionmain.html', context_dict, context)
