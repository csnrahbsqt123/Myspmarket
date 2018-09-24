# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-22 05:32
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='昵称')),
                ('gender', models.SmallIntegerField(choices=[(1, '男'), (2, '女'), (3, '保密')], default=1, verbose_name='性别')),
                ('school', models.CharField(blank=True, max_length=20, null=True, verbose_name='学校')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='地址')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='生日')),
                ('home', models.CharField(blank=True, max_length=30, null=True, verbose_name='故乡')),
                ('mobile', models.CharField(max_length=18, unique=True, validators=[django.core.validators.RegexValidator('^1[3-9]\\d{9}$', '手机号码格式错误')], verbose_name='手机号或用户名')),
                ('pwd', models.CharField(max_length=64, validators=[django.core.validators.MinLengthValidator(6)], verbose_name='登录密码')),
            ],
            options={
                'db_table': 'person',
            },
        ),
    ]
