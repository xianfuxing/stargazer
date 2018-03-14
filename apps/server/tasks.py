from __future__ import absolute_import, unicode_literals
from celery import task


@task()
def update_ecs_status():
    print('Update ecs status')
    return 'ecs'
