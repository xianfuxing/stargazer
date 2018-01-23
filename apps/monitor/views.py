import datetime
from collections import OrderedDict
from django.http import JsonResponse
from django.views.generic import View

from .mixins.zapi import ZapiMixin


class HostidDetailView(ZapiMixin, View):
    def get(self, request, host_name):
        hostid_resp = self.get_hostid(host_name)
        return JsonResponse(hostid_resp)

    def get_hostid(self, host_name):
        zapi = self.get_zapi()
        try:
            resp = zapi.host.get(filter={'host':[host_name]}, output=['hostid', 'name'])
            resp = resp[0]
        except IndexError:
            resp = {'hostid': '', 'name': ''}

        return resp


class ItemDetailView(HostidDetailView):
    def get(self, request, host_name, item_key):
        item_resp = self.get_itemid(host_name, item_key)

        return JsonResponse(item_resp)

    def get_itemid(self, host_name, item_key):
        zapi = self.get_zapi()
        hostid_resp = self.get_hostid(host_name)
        if not hostid_resp['hostid']:
            return {'hostid': '', 'name': '', 'lastvalue': ''}

        # Get hostid
        hostid = hostid_resp['hostid']
        item_resp = zapi.item.get(search={'key_': 'system.cpu.util[,{0}]'.format(item_key)},
                             hostids=hostid,
                             output=['hostid', 'itemid', 'lastvalue'])
        if item_resp:
            return item_resp[0]
        else:
            return {'itemid': '', 'hostid': '', 'lastvalue': ''}


class HistoryDetailView(ItemDetailView):
    def get(self, request, host_name, item_key):
        item_resp = self.get_itemid(host_name, item_key)
        if not item_resp['itemid']:
            return JsonResponse({'clock': '', 'value': ''})

        itemid = item_resp['itemid']
        zapi = self.get_zapi()
        history_resp = zapi.history.get(itemids=itemid,
                                        output='extend',
                                        sortfield='clock',
                                        sortorder='ASC',
                                        limit=10,
                                        history=0)
        if history_resp:
            _history_resp = []
            for item in history_resp:
                _history_resp.append((item['clock'], item['value']))
            _history_resp = OrderedDict(_history_resp)
            return JsonResponse(_history_resp)
        else:
            return JsonResponse({'clock':'', 'value': ''})
