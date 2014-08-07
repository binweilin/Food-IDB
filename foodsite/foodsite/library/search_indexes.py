from haystack import indexes
from foodsite.library.models import Chef, Region, Recipe

class RegionIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    # name = indexes.CharField(model_attr='name')
    # image = indexes.TextField(model_attr='image')
    # description = indexes.CharField(model_attr='description')
    # google_map = indexes.TextField(model_attr='google_map')

    def get_model(self):
        return Region

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class ChefIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    # name = indexes.CharField(model_attr='name')
    # image = indexes.TextField(model_attr='image')
    # description = indexes.CharField(model_attr='description')
    # google_map = indexes.TextField(model_attr='google_map')

    def get_model(self):
        return Chef

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class RecipeIndex(indexes.SearchIndex, indexes.Indexable):

    text = indexes.CharField(document=True, use_template=True)
    # name = indexes.CharField(model_attr='name')
    # image = indexes.TextField(model_attr='image')
    # description = indexes.CharField(model_attr='description')
    # google_map = indexes.TextField(model_attr='google_map')

    def get_model(self):
        return Recipe

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
