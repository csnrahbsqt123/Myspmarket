# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-24 07:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_sendimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='logo',
            field=models.ImageField(default='logo/2018/09/24/infortx.png', upload_to='logo/%Y/%m/%d', verbose_name='LOGO'),
        ),
    ]