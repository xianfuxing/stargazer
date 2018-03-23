from django.contrib import admin
from .models import SslCertificate


class SslAdmin(admin.ModelAdmin):
    list_display = ('domain', 'issuer', 'cert_type', 'validity', 'expiry_date')
    list_filter = ('domain', 'issuer', 'cert_type')
    ordering = ['domain']


admin.site.register(SslCertificate, SslAdmin)
