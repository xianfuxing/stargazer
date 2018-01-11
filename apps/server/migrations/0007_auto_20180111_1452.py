# Generated by Django 2.0 on 2018-01-11 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0006_host_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='region',
            field=models.CharField(default='华南', max_length=10, verbose_name='所在可用区'),
        ),
        migrations.AlterField(
            model_name='host',
            name='status',
            field=models.CharField(choices=[('running', '运行中'), ('stopped', '已停止'), ('retired', '已退役')], default='running', max_length=10, verbose_name='运行状态'),
        ),
    ]