from django.shortcuts import render, HttpResponse
from django.views.generic import View

from .mixins.zapi import ZapiMixin


class HostidView(ZapiMixin, View):
    def get(self, request, host_name):
        zapi = self.get_zapi()

        resp_list = zapi.host.get(filter={'host':[host_name]}, output=['hostid', 'name'])
        resp = resp_list[0]
        return HttpResponse(resp, content_type='application/json')