import random
import numpy as np
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.views.generic import TemplateView, ListView, DeleteView
from pure_pagination.mixins import PaginationMixin

from .mixins.page_cache import CacheMixin
from .models import Host, Org


class DashboardView(TemplateView):
    # cache_timeout = 300
    template_name = 'server/dashboard.html'


class ServerOverviewView(CacheMixin, ListView):
    model = Org
    pk_url_kwarg = 'org_list'
    cache_timeout = 300
    template_name = 'server/overview.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=None, **kwargs)
        ctx['host_count'] = Host.objects.all().count()
        ctx['is_stopped'] = Host.objects.filter(status='stopped').count()
        return ctx


class ServerListView(PaginationMixin, ListView):
    # cache_timeout = 300
    model = Host
    context_object_name = 'hosts'
    template_name = 'server/host_list.html'

    paginate_by = 5
    object = Host

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
        org = self.request.GET.get('org', '')
        due = self.request.GET.get('due', '')
        if org:
            query_set = query_set.filter(org=org)

        if status == 'stopped' or status == 'running':
            query_set = query_set.filter(status=status)

        if due == 'soon':
            if query_set:
                return [host for host in query_set if host.will_be_expired]
        elif due == 'yes':
            if query_set:
                return [host for host in query_set if host.is_expired]
        else:
            return query_set

        return query_set

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=None, **kwargs)
        host_count = Host.objects.all().count()
        ctx['host_count'] = host_count

        return ctx


class ServerDetailView(DeleteView):
    pk_url_kwarg = 'host_id'
    model = Host
    context_object_name = 'host'
    template_name = 'server/host_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        return ctx


def index(request):
    return render(request, 'server/index.html')
