from django.contrib import admin
from .models import Host, Service, Org, HostHardware
# Register your models here.


class HostAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'ip', 'org',
                    'provider', 'platform', 'price', 'expiration_date')
    list_filter = ('hostname', 'ip', 'provider', 'platform', 'expiration_date')
    date_hierarchy = 'expiration_date'
    ordering = ['hostname', 'expiration_date']


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'port', 'version')
    list_filter = ('name', 'port')
    ordering = ['name']


class OrgAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    list_filter = ('name', 'code')
    ordering = ['name']


class HostHardwareAdmin(admin.ModelAdmin):
    list_display = ('version', 'specific', 'cpu', 'memory')
    list_filter = ('version', 'specific', 'cpu', 'memory')
    ordering = ['version']


admin.site.register(Host, HostAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Org, OrgAdmin)
admin.site.register(HostHardware, HostHardwareAdmin)