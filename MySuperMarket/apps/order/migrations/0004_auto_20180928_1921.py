# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-28 11:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20180928_1114'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraddress',
            name='row_id',
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='city_id',
            field=models.CharField(blank=True, default='', max_length=100, verbose_name='市id'),
        ),
    ]