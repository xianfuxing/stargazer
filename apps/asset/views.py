from django.shortcuts import Http404, redirect
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import SslCertificate

from pure_pagination.mixins import PaginationMixin


class AssetOverviewView(LoginRequiredMixin, TemplateView):
    template_name = 'asset/overview.html'


class SslListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = SslCertificate
    context_object_name = 'ssl_list'
    template_name = 'asset/ssl_list.html'

    paginate_by = 6
    object = SslCertificate

    def get(self, request, *args, **kwargs):
        request = self.request
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            if request.GET.get('page', 1) == 1:
                raise

        _page = request.GET.copy()
        del _page['page']
        params = _page.urlencode()
        if params:
            return redirect('%s?%s' % (request.path, params))
        else:
            return redirect('%s' % request.path)

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.order_by('domain')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ssl_count = SslCertificate.objects.all().count()
        ctx['ssl_count'] = ssl_count

        return ctx
