from django.db import models
from django.utils import timezone

# Create your models here.


class Org(models.Model):
    name = models.CharField(max_length=20, verbose_name='组织名称')
    code = models.CharField(max_length=10, verbose_name='组织代码')
    desc = models.CharField(max_length=100, blank='True', verbose_name='描述')

    class Meta:
        verbose_name = '组织'
        verbose_name_plural = verbose_name

    def get_running_count(self):
        return self.host_set.filter(status='running').count()

    def get_stopped_count(self):
        return self.host_set.filter(status='stopped').count()

    def get_retired_count(self):
        return self.host_set.filter(status='retired').count()

    def get_all_count(self):
        return self.host_set.all().count()

    def __str__(self):
        return self.name


class HostHardware(models.Model):
    version = models.CharField(max_length=30, verbose_name='实例规格')
    cpu = models.IntegerField(verbose_name='处理器')
    memory = models.IntegerField(verbose_name='内存')

    class Meta:
        verbose_name = '配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.version


class Host(models.Model):
    STATUS_CHOICES = (
        ('running', '运行中'),
        ('stopped', '已停止'),
        ('retired', '已退役'),
    )
    hostname = models.CharField(max_length=50, verbose_name='主机名')
    ip = models.GenericIPAddressField(verbose_name='ip地址')
    desc = models.CharField(max_length=200, default='', blank=True, verbose_name='描述')
    org = models.ForeignKey(Org, verbose_name='所在组织', on_delete='PROTECT')
    region = models.CharField(max_length=10, default='华南', verbose_name='所在可用区')
    # hardware = models.CharField(max_length=200, verbose_name='硬件配置')
    hardware = models.ForeignKey(HostHardware, verbose_name='硬件配置', default=1, on_delete='PROTECT')
    provider = models.CharField(default='阿里云', max_length=50, verbose_name='服务商')
    platform = models.CharField(default='Linux', max_length=50, verbose_name='平台')
    status = models.CharField(default='running', max_length=10, choices=STATUS_CHOICES, verbose_name='运行状态')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '主机'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.hostname


class Service(models.Model):
    host = models.ManyToManyField(Host, verbose_name='所属服务器')
    name = models.CharField(max_length=50, verbose_name='服务')
    port = models.IntegerField(verbose_name='端口')
    version = models.CharField(max_length=20, verbose_name='版本')

    class Meta:
        verbose_name = '服务'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name