from django.contrib import admin
from foodsite.library.models import Region, Chef, Recipe

admin.site.register(Region)
admin.site.register(Chef)
admin.site.register(Recipe)