# Generated by Django 2.0 on 2018-01-16 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0030_remove_host_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True, verbose_name='年费'),
        ),
    ]
