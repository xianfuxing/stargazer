# Generated by Django 2.0 on 2018-01-16 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0021_auto_20180116_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='price',
            field=models.DecimalField(decimal_places=2, default=10000.0, max_digits=2, verbose_name='年费'),
        ),
    ]
