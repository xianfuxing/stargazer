import os
from django.db import models
from django.contrib.auth.models import AbstractUser

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


def mugshot_path(instance, filename):
    return os.path.join('mugshots', instance.username, filename)


class User(AbstractUser):
    phone = models.CharField(max_length=11, null=True, blank=True, default='', verbose_name='电话')
    department = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='部门')
    position = models.CharField(max_length=50, null=True, blank=True, default='', verbose_name='职位')
    mugshot = models.ImageField(upload_to=mugshot_path, null=True, blank=True)
    mugshot_thumbnail = ImageSpecField(source='mugshot',
                                       processors=[ResizeToFill(100, 100)],
                                       format='JPEG',
                                       options={'quality': 100})

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def mugshot_url(self):
        return self.mugshot_thumbnail.url

    def __str__(self):
        return self.username
