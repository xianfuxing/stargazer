from django.contrib import admin
from .models import Host, Service, Org
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


class OrgAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    list_filter = ('name', 'code')
    ordering = ['name']


admin.site.register(Host, HostAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Org, OrgAdmin)