from django.db import models
from django.utils import timezone


class SslCertificate(models.Model):
    domain = models.CharField(max_length=50, verbose_name='证书域名')
    description = models.CharField(max_length=100, null=True, blank=True, verbose_name='描述')
    issuer = models.CharField(max_length=50, null=True, blank=True, verbose_name='颁发商')
    cert_type = models.CharField(max_length=50, null=True, blank=True, verbose_name='证书类型')
    validity = models.PositiveIntegerField(verbose_name='有效期')
    expiry_date = models.DateTimeField(default=timezone.now, verbose_name='到期时间')

    class Meta:
        verbose_name = '证书信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.domain
