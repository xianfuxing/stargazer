import datetime
from collections import OrderedDict
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from server.models import Host

from .mixins.zapi import ZapiMixin


class HostDetailView(LoginRequiredMixin, ZapiMixin, View):
    def get(self, request, host_name, *args, **kwargs):
        host_reps = self.get_host(host_name)
        return JsonResponse(host_reps)

    def get_host(self, host_name=None, **kwargs):
        zapi = self.get_zapi()
        try:
            if host_name:
                host_resp = zapi.host.get(filter={'host': [host_name]}, output=['hostid', 'name'], **kwargs)
            else:
                host_resp = zapi.host.get(output=['hostid', 'name'], **kwargs)
            host_resp = host_resp[0]
        except IndexError:
            host_resp = {'hostid': '', 'name': ''}
        return host_resp

    @staticmethod
    def get_host_object(host_name):
        try:
            host = Host.objects.get(hostname=host_name)
        except Host.DoesNotExist:
            return {'msg': 'host is not exist'}

        return host


class ItemDetailView(HostDetailView):
    def get(self, request, host_name, *args, **kwargs):
        item_type, item_key = kwargs['item_type'], kwargs['item_key']
        item_resp = self.get_item(host_name, item_type, item_key)

        return JsonResponse(item_resp)

    def get_item(self, host_name, item_type, item_key):
        host = self.get_host_object(host_name)
        item_type_map = {
            "cpu": "system.cpu.util[,{0}]",
            "disk": "vfs.fs.size[{0}".format(host.disk_name)+",{0}]"
        }

        if host.platform.lower() == 'windows':
            item_type_map.update({'cpu': 'perf_counter[\Processor(_Total)\% Idle Time]'})

        zapi = self.get_zapi()
        host_reps = self.get_host(host_name)
        if not host_reps['hostid']:
            return {'hostid': '', 'name': '', 'lastvalue': ''}

        # Get hostid
        host_id = host_reps['hostid']

        # Get item_type
        item_type = item_type_map.get(item_type, '')
        # If item_tpe is exist return item_resp
        if item_type:
            item_resp = zapi.item.get(
                search={'key_': item_type.format(item_key)},
                hostids=host_id,
                output=['lastclock', 'itemid', 'lastvalue'])
        else:
            return {'itemid': '', 'lastclock': '', 'lastvalue': ''}

        # Return item response if is not empty
        if item_resp:
            return item_resp[0]
        else:
            return {'itemid': '', 'lastclock': '', 'lastvalue': ''}


class HistoryDetailView(ItemDetailView):
    def get(self, request, host_name, *args, **kwargs):
        host = self.get_host_object(host_name)
        item_type, item_key = kwargs['item_type'], kwargs['item_key']
        item_resp = self.get_item(host_name, item_type, item_key)
        if item_resp.get('itemid', '') == '':
            return JsonResponse({'clock': '', 'value': ''})

        itemid = item_resp['itemid']
        zapi = self.get_zapi()

        end = datetime.datetime.now()
        start = end - datetime.timedelta(0, 3600)

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
                # for windows server
                # if host.platform.lower() == 'windows':
                #     value = round(float(item['value']), 2)
                _history_resp.append((time, value))
            _history_resp = OrderedDict(_history_resp)
            data = [{'name': time, 'value': [time, value]} for time, value in _history_resp.items()]
            history_data = {'data': data}

            return JsonResponse(history_data)
        else:
            return JsonResponse({'data': []})


class TriggerListView(HostDetailView):
    def get(self, request, *args, **kwargs):
        trigger_resp = {}
        zapi = self.get_zapi()
        trigger_list = zapi.trigger.get(filter={'value': 1}, output=['triggerid', 'description', 'value', 'lastchange'])
        if trigger_list:
            for trigger in trigger_list:
                triggerid = trigger['triggerid']

                # Get hostname
                try:
                    hostname = self.get_host(triggerids=triggerid)['name']
                except KeyError:
                    hostname = None

                # Get trigger resp
                try:
                    trigger_resp[hostname] += [trigger]
                except KeyError:
                    trigger_resp[hostname] = [trigger]
        return JsonResponse(trigger_resp)


class MonitorListView(LoginRequiredMixin, TemplateView):
    template_name = 'monitor/monitor_list.html'
