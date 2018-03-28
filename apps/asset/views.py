import requests
import json
import urllib3
from django.shortcuts import Http404, redirect
from django.http import JsonResponse
from django.conf import settings
from django.views.generic import View, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import SslCertificate
from .tasks import get_ssl_info
from .utils import get_salt_resp_stdout

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
        status = self.request.GET.get('status', '')
        if status == 'danger':
            if query_set:
                to_expire = SslCertificate.to_expire.all()
                is_expired = SslCertificate.is_expired.all()
                query_set = to_expire.union(is_expired)
        return query_set.order_by('domain')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ssl_count = SslCertificate.objects.all().count()
        ctx['ssl_count'] = ssl_count

        return ctx


class SlsRenewView(LoginRequiredMixin, View):
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
            try:
                ssl = SslCertificate.objects.get(domain=domain)
            except SslCertificate.DoesNotExist:
                return JsonResponse({'domain': domain, 'msg': 'domain is not existed'})
            # salt-api authenticate
            session = requests.Session()
            # disable ssl check warning
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            session.post(salt_url + 'login', json={'username': salt_username,
                                                   'password': salt_password,
                                                   'eauth': 'pam'
                                                   }, verify=False)
            # send renew request
            resp = session.post(salt_url, json=[{'client': 'local',
                                                 'tgt': ssl.host.hostname,
                                                 'fun': 'state.sls',
                                                 'arg': 'ssl.renew',
                                                 'kwarg': {'pillar': {'domain': domain}}}], verify=False)
            data = json.loads(resp.text)
            try:
                data = data['return'][0]
                resp = get_salt_resp_stdout(data)
                stdout, stderr, result = resp['stdout'], resp['stderr'], resp['result']
            except KeyError:
                return JsonResponse({'domain': domain, 'msg': 'result not found'})
            if result:
                msg = 'not due' if 'not due' in stdout else 'renewed'
            else:
                if stderr:
                    msg = 'No certificate found' if 'No certificate found' in stderr else 'unknown error'
            return JsonResponse({'domain': domain, 'msg': msg})
        return JsonResponse({'domain': '', 'msg': 'domain is none'})
