from haystack import indexes
from .models import Host


class HostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Host

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
