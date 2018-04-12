import os
from django.db import models
from django.contrib.auth.models import AbstractUser

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.exceptions import MissingSource


def avatar_path(instance, filename):
    return os.path.join('avatar', instance.username, filename)


class User(AbstractUser):
    phone = models.CharField(max_length=11, null=True, blank=True, default='', verbose_name='电话')
    department = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='部门')
    position = models.CharField(max_length=50, null=True, blank=True, default='', verbose_name='职位')
    avatar = models.ImageField(upload_to=avatar_path, null=True, blank=True)
    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(100, 100)],
                                      format='JPEG',
                                      options={'quality': 100})

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def avatar_url(self):
        try:
            avatar_thumbnail_url = self.avatar_thumbnail.url
        except MissingSource:
            avatar_thumbnail_url = ''
        return avatar_thumbnail_url

    def __str__(self):
        return self.username
