import requests
from django.shortcuts import Http404, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.generic import View, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import SslCertificate
from .tasks import get_ssl_info

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


class SlsRenewView(View):
    def get(self, request, *args, **kwargs):
        request = self.request
        domain = request.GET.get('domain', '')
        return JsonResponse({'domain': domain, 'msg': ''})

    def post(self, request, *args, **kwargs):
        salt_url = getattr(settings, 'SALT_URL', '')
        salt_username = getattr(settings, 'SALT_USER', '')
        salt_password = getattr(settings, 'SALT_PASSWORD', '')
        request = self.request
        domain = request.POST.get('domain', request.GET.get('domain'))
        if domain:
            session = requests.Session()
            session.post(salt_url+'login', json={'username': salt_username,
                                                               'password': salt_password,
                                                               'eauth': 'pam'
                                                               }, verify=False)
            resp = session.post(salt_url, json=[{'client': 'local',
                                          'tgt': 'new-aiyou',
                                          'fun': 'state.sls',
                                          'arg': 'ssl.renew'}], verify=False)
            data = resp.content
            return HttpResponse(data, content_type='application/json')
        return JsonResponse({'domain': '', 'msg': ''})