# Generated by Django 2.0 on 2018-01-16 06:43

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0031_host_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='price',
            field=models.DecimalField(decimal_places=2, default=Decimal('90000'), max_digits=7, verbose_name='年费'),
        ),
    ]
