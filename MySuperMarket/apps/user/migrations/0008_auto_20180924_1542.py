# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-24 07:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20180924_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='logo',
        ),
        migrations.AddField(
            model_name='person',
            name='head',
            field=models.ImageField(default='logo/2018/09/24/tx1.png', upload_to='logo/%Y/%m/%d', verbose_name='head'),
        ),
    ]
