# Generated by Django 2.0 on 2018-03-12 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='instance_id',
            field=models.CharField(default=123, max_length=50, verbose_name='实例id'),
            preserve_default=False,
        ),
    ]
