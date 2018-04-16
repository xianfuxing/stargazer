from .. import settings_secret
from django.core.cache import cache
from pyzabbix import ZabbixAPI


class ZapiMixin(object):
    """
     Mixin for return zapi
    """
    @staticmethod
    def get_zapi():
        # Get zapi cache if exist
        zapi = cache.get('zapi')
        if zapi:
            return zapi

        ZAPI_URL = getattr(settings_secret, 'ZAPI_URL', '')
        ZAPI_USER = getattr(settings_secret, 'ZAPI_USER', '')
        ZAPI_PASSWORD = getattr(settings_secret, 'ZAPI_PASSWORD', '')
        zapi = ZabbixAPI(ZAPI_URL)
        zapi.login(ZAPI_USER, ZAPI_PASSWORD)

        # Cache zapi if not hit
        cache.set('zapi', zapi, 600)
        return zapi
