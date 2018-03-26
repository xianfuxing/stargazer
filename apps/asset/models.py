from django.db import models
from django.utils import timezone


class SslCertificate(models.Model):
    MIDDLEMAN_CHOICES = (
        ('qcloud', '腾讯云'),
        ('aliyun', '阿里云'),
        ('qiniu', '七牛'),
        ('certbot', 'certbot'),
        ('other', 'other')
    )
    domain = models.CharField(max_length=50, verbose_name='证书域名')
    description = models.CharField(max_length=100, null=True, blank=True, verbose_name='描述')
    middleman = models.CharField(max_length=50, default='', choices=MIDDLEMAN_CHOICES, verbose_name='代理商')
    issuer = models.CharField(max_length=50, null=True, blank=True, verbose_name='颁发商')
    cert_type = models.CharField(max_length=50, null=True, blank=True, verbose_name='证书类型')
    validity = models.PositiveIntegerField(verbose_name='有效期')
    expiry_date = models.DateTimeField(default=timezone.now, verbose_name='到期时间')
    host = models.ForeignKey('server.Host', on_delete='PROTECT', verbose_name='所在服务器')

    class Meta:
        verbose_name = '证书信息'
        verbose_name_plural = verbose_name

    @property
    def will_be_expired(self):
        timedelta = self.expiry_date - timezone.now()
        return timezone.timedelta(0) <= timedelta <= timezone.timedelta(days=14)

    @property
    def is_expired(self):
        timedelta = self.expiry_date - timezone.now()
        return timedelta < timezone.timedelta(0)

    def __str__(self):
        return self.domain
