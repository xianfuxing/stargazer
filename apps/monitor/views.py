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

    def get(self, request, host_name, item_type, item_key):
        item_resp = self.get_itemid(host_name, item_type, item_key)

        return JsonResponse(item_resp)

    def get_itemid(self, host_name, item_type, item_key):
        item_type_map = {
            "cpu": "system.cpu.util[,{0}]",
        }
        zapi = self.get_zapi()
        hostid_resp = self.get_hostid(host_name)
        if not hostid_resp['hostid']:
            return {'hostid': '', 'name': '', 'lastvalue': ''}

        # Get hostid
        hostid = hostid_resp['hostid']

        # Get item_type
        item_type = item_type_map.get(item_type, '')
        # If item_tpe is exist return item_resp
        if item_type:
            item_resp = zapi.item.get(search={'key_': item_type.format(item_key)},
                             hostids=hostid,
                             output=['lastclock', 'itemid', 'lastvalue'])
        else:
            return {'itemid': '', 'lastclock': '', 'lastvalue': ''}

        # Return item response if is not empty
        if item_resp:
            return item_resp[0]
        else:
            return {'itemid': '', 'lastclock': '', 'lastvalue': ''}


class HistoryDetailView(ItemDetailView):
    def get(self, request, host_name, item_type, item_key):
        item_resp = self.get_itemid(host_name, item_type, item_key)
        if not item_resp['itemid']:
            return JsonResponse({'clock': '', 'value': ''})

        itemid = item_resp['itemid']
        zapi = self.get_zapi()

        end = datetime.datetime.now()
        start = end - datetime.timedelta(0,3600)

        # to timestamp
        end = end.timestamp()
        start = start.timestamp()
        history_resp = zapi.history.get(itemids=itemid,
                                        output='extend',
                                        sortfield='clock',
                                        sortorder='ASC',
                                        history=0,
                                        time_from=start,
                                        time_till=end)
        if history_resp:
            _history_resp = []
            for item in history_resp:
                dt = datetime.datetime.fromtimestamp(float(item['clock']))
                time = dt.strftime('%Y/%m/%d %H:%M:%S')
                value = round(100 - float(item['value']), 2)
                _history_resp.append((time, value))
            _history_resp = OrderedDict(_history_resp)
            data = [{'name': time, 'value':[time, value]} for time, value in _history_resp.items()]
            history_data = {'data': data}

            return JsonResponse(history_data)
        else:
            return JsonResponse({'data': []})


class TriggerListView(ZapiMixin, View):
    pass