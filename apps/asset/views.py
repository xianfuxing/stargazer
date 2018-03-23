from django.views.generic import TemplateView, ListView
from .models import SslCertificate


class AssetOverviewView(TemplateView):
    template_name = 'asset/overview.html'


class SslListView(ListView):
    model = SslCertificate
    context_object_name = 'ssl_list'
    template_name = 'asset/ssl_list.html'
