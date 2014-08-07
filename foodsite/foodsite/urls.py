from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from foodsite.library import views
# from api import ChefResource

from django.contrib import admin
admin.autodiscover()

# chef_resource = ChefResource()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    (r'^index/', TemplateView.as_view(template_name="index.html")),
    (r'^$', TemplateView.as_view(template_name="index.html")),
    # (r'^chefs/gordon_ramsay', TemplateView.as_view(template_name="chefs/gordon_ramsay.html")),
    (r'^about/', TemplateView.as_view(template_name="about.html")),
    (r'^chefs/$', views.chefmain),
    (r'^recipes/$', views.recipemain),
    (r'^regions/$', views.regionmain),
    (r'^sochi/$', views.sochimain),
    (r'^recipes/(?P<recipe_name_url>\w+)/$', views.recipe),
    (r'^chefs/(?P<chef_name_url>\w+)/$', views.chef),
    (r'^regions/(?P<region_name_url>\w+)/$', views.region),
    (r'^api/chef/(?P<chef_pk>\w+)?', views.get_chef),
    (r'^api/region/(?P<region_pk>\w+)?', views.get_region),
    (r'^api/recipe/(?P<recipe_pk>\w+)?', views.get_recipe),
    (r'^search/', include('haystack.urls')),
    (r'^search/search_result/?', views.search),
)