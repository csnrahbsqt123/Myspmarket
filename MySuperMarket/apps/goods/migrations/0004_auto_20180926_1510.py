# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-26 07:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20180925_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='url_site',
            field=models.CharField(max_length=200, null=True, verbose_name='活动的url地址'),
        ),
    ]
