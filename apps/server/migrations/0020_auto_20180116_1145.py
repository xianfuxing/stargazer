# Generated by Django 2.0 on 2018-01-16 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0019_auto_20180116_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=2, null=True, verbose_name='年费'),
        ),
    ]
