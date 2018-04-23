from django.shortcuts import render, redirect
from django.http import JsonResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView, ListView, DetailView
from pure_pagination.mixins import PaginationMixin
from haystack.query import SearchQuerySet
from django.core import serializers

from .mixins.page_cache import CacheMixin
from .models import Host, Org


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'server/dashboard.html'


class ServerOverviewView(LoginRequiredMixin, ListView):
    model = Org
    pk_url_kwarg = 'org_list'
    template_name = 'server/overview.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(object_list=None, **kwargs)
        ctx['host_count'] = Host.objects.all().count()
        ctx['is_stopped'] = Host.objects.filter(status='stopped').count()
        return ctx


class ServerListView(LoginRequiredMixin, PaginationMixin, ListView):
    model = Host
    context_object_name = 'hosts'
    template_name = 'server/host_list.html'

    paginate_by = 8
    object = Host

    def get(self, request, *args, **kwargs):
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
        query = self.request.GET.get('q', '')
        if org:
            query_set = query_set.filter(org=org)

        if status == 'stopped' or status == 'running':
            query_set = query_set.filter(status=status)

        if due == 'soon':
            if query_set:
                query_set = Host.to_expire_objects.all()
        elif due == 'yes':
            if query_set:
                query_set = Host.is_expired_objects.all()
        else:
            query_set.order_by('hostname')

        if query:
            results = SearchQuerySet().models(Host).filter(content=query).load_all()
            query_set = [result.object for result in results]

        return query_set

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        host_count = Host.objects.all().count()
        ctx['host_count'] = host_count
        ctx['query'] = self.request.GET.get('q', '')

        return ctx


class ServerDetailView(LoginRequiredMixin, DetailView):
    pk_url_kwarg = 'host_id'
    model = Host
    context_object_name = 'host'
    template_name = 'server/host_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        return ctx


class ServerSearchView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q', '')
        if query:
            results = SearchQuerySet().models(Host).filter(content=query).load_all()
            host_queryset = [result.object for result in results]
            host_list = serializers.serialize('json', host_queryset)
            return JsonResponse({'results': host_list, 'success': True})
        else:
            return JsonResponse({'results': [], 'msg': 'Please enter keyword', 'success': False})
