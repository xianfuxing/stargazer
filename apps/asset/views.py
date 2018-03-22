from django.views.generic import TemplateView


class AssetOverviewView(TemplateView):
    template_name = 'asset/overview.html'
