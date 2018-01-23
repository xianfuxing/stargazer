from django.conf import settings
from pyzabbix import ZabbixAPI


class ZapiMixin(object):
    """
     Mixin for return zapi
    """
    def get_zapi(self):
        ZAPI_URL = getattr(settings, 'ZAPI_URL', '')
        ZAPI_USER = getattr(settings, 'ZAPI_USER', '')
        ZAPI_PASSWORD = getattr(settings, 'ZAPI_PASSWORD', '')
        zapi = ZabbixAPI(ZAPI_URL)
        zapi.login(ZAPI_USER, ZAPI_PASSWORD)

        return zapi