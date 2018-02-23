from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    department = models.CharField(max_length=20, default='', verbose_name='部门')
    position = models.CharField(max_length=50, default='', verbose_name='职位')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
