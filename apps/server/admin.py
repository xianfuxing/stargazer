from django.contrib import admin
from .models import Host, Service
# Register your models here.


class HostAdmin(admin.ModelAdmin):
    list_display = ('hostname', 'ip', 'org',
                    'provider', 'platform', 'create_time')
    list_filter = ('hostname', 'ip', 'provider', 'platform', 'create_time')
    date_hierarchy = 'create_time'
    ordering = ['hostname', 'create_time']


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'port', 'version')
    list_filter = ('name', 'port')
    ordering = ['name']


admin.site.register(Host, HostAdmin)
admin.site.register(Service, ServiceAdmin)