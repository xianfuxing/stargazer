from django.db import models
from django.utils import timezone

# Create your models here.


class Host(models.Model):
    ORG_CHOICES = (
        ('YJH', '优计划'),
        ('TBS', '淘巴士'),
        ('CST', '商家')
    )

    STATUS_CHOICES = (
        ('running', '运行中'),
        ('stopped', '已停止'),
        ('retired', '已退役'),
    )
    hostname = models.CharField(max_length=50, verbose_name='主机名')
    ip = models.GenericIPAddressField(verbose_name='ip地址')
    desc = models.CharField(max_length=200, default='', verbose_name='描述')
    org = models.CharField(max_length=5, choices=ORG_CHOICES, verbose_name='所在组织')
    region = models.CharField(max_length=10, default='华南', verbose_name='所在可用区')
    hardware = models.CharField(max_length=200, default='', blank=True, verbose_name='硬件配置')
    provider = models.CharField(default='阿里云', max_length=50, verbose_name='服务商')
    platform = models.CharField(default='Linux', max_length=50, verbose_name='平台')
    status = models.CharField(default='running', max_length=10, choices=STATUS_CHOICES, verbose_name='运行状态')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    def __str__(self):
        return self.hostname


class Service(models.Model):
    host = models.ManyToManyField(Host, verbose_name='所属服务器')
    name = models.CharField(max_length=50, verbose_name='服务')
    port = models.IntegerField(verbose_name='端口')
    version = models.CharField(max_length=20, verbose_name='版本')

    def __str__(self):
        return self.name