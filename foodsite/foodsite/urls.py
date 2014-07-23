from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from foodsite.library import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^index/', TemplateView.as_view(template_name="index.html")),
    (r'^$', TemplateView.as_view(template_name="index.html")),
    # (r'^chefs/gordon_ramsay', TemplateView.as_view(template_name="chefs/gordon_ramsay.html")),
    # (r'^chefs/paula_deen', TemplateView.as_view(template_name="chefs/paula_deen.html")),
    # (r'^chefs/masaharu_morimoto', TemplateView.as_view(template_name="chefs/masaharu_morimoto.html")),
    # (r'^chefs/', TemplateView.as_view(template_name="chefs.html")),
    # (r'^regions/southern_usa', TemplateView.as_view(template_name="regions/southern_usa.html")),
    # (r'^regions/japan', TemplateView.as_view(template_name="regions/japan.html")),
    # (r'^regions/great_britain', TemplateView.as_view(template_name="regions/great_britain.html")),
    # (r'^regions/', TemplateView.as_view(template_name="regions.html")),
    # (r'^recipes/southern_fried_chicken', TemplateView.as_view(template_name="recipes/southern_fried_chicken.html")),
    # (r'^recipes/unagi_roll', TemplateView.as_view(template_name="recipes/unagi_roll.html")),
    # (r'^recipes/vegetable_sushi', TemplateView.as_view(template_name="recipes/vegetable_sushi.html")),
    # (r'^recipes/pork_and_ham_pie', TemplateView.as_view(template_name="recipes/pork_and_ham_pie.html")),
    # (r'^recipes/', TemplateView.as_view(template_name="recipes.html")),
    (r'^about/', TemplateView.as_view(template_name="about.html")),
    (r'^index2/', views.index2),
    (r'^chefs/$', views.chefmain),
    (r'^recipes/$', views.recipemain),
    (r'^regions/$', views.regionmain),
    (r'^recipes/(?P<recipe_name_url>\w+)/$', views.recipe),
    (r'^chefs/(?P<chef_name_url>\w+)/$', views.chef),
    (r'^regions/(?P<region_name_url>\w+)/$', views.region),

)