from tastypie.resources import ModelResource
from foodsite.models import Chef, Recipe, Region

class ChefResource(ModelResource):
    class Meta:
        queryset = Chef.objects.all()
        resource_name = 'chef'


