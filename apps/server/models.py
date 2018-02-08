from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, ValidationError

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

    def get_all_count(self):
        return self.host_set.all().count()

    def get_will_be_expired_count(self):
        host_set = self.host_set.all()
        self.will_be_expired_count = 0
        for host in host_set:
            if host.will_be_expired:
                self.will_be_expired_count += 1
        return self.will_be_expired_count

    def get_is_expired_count(self):
        host_set = self.host_set.all()
        self.is_expired_count = 0
        for host in host_set:
            if host.is_expired:
                self.is_expired_count += 1
        return self.is_expired_count

    def __str__(self):
        return self.name


class HostHardware(models.Model):
    version = models.CharField(max_length=30, unique=True, verbose_name='实例规格')
    specific = models.CharField(max_length=20, verbose_name='规格族')
    cpu = models.PositiveIntegerField(verbose_name='处理器', validators=[MinValueValidator(1, message='最小为1')])
    memory = models.PositiveIntegerField(verbose_name='内存', validators=[MinValueValidator(1, message='最小为1')])

    class Meta:
        verbose_name = '配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.version


class Host(models.Model):
    STATUS_CHOICES = (
        ('running', '运行中'),
        ('stopped', '已停止'),
    )

    PAY_CHOICES = (
        ('reserved', '包年包月'),
        ('on_demand', '按量付费')
    )
    hostname = models.CharField(max_length=50, verbose_name='主机名')
    ip = models.GenericIPAddressField(verbose_name='ip地址')
    desc = models.CharField(max_length=200, default='', blank=True, verbose_name='描述')
    org = models.ForeignKey(Org, verbose_name='所在组织', on_delete='PROTECT')
    region = models.CharField(max_length=10, default='华南', verbose_name='所在可用区')
    hardware = models.ForeignKey(HostHardware, verbose_name='硬件配置', default=1, on_delete='PROTECT')
    provider = models.CharField(default='阿里云', max_length=50, verbose_name='服务商')
    platform = models.CharField(default='Linux', max_length=50, verbose_name='平台')
    pay_method = models.CharField(max_length=10, default='reserved', choices=PAY_CHOICES, verbose_name='付费方式')
    expiration_date = models.DateTimeField(default=timezone.now, verbose_name='到期时间')
    price = models.DecimalField(default=Decimal('0'), max_digits=7, decimal_places=2, verbose_name='年费')
    status = models.CharField(default='running', max_length=10, choices=STATUS_CHOICES, verbose_name='运行状态')
    create_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name = '主机'
        verbose_name_plural = verbose_name

    @property
    def will_be_expired(self):
        timedelta = self.expiration_date - timezone.now()
        return timezone.timedelta(0) <= timedelta <= timezone.timedelta(days=30)

    @property
    def is_expired(self):
        timedelta = self.expiration_date - timezone.now()
        return timedelta < timezone.timedelta(0)

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