# Generated by Django 2.0 on 2018-01-16 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0026_auto_20180116_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1000.00, max_digits=7, verbose_name='年费'),
            preserve_default=False,
        ),
    ]