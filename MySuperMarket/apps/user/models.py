from django.core import validators
from django.db import models

# Create your models here.
from db.base_model import BaseModel


class Person(BaseModel):
    set = ((1, "男"), (2, "女"), (3, "保密"))
    head = models.ImageField(upload_to='head/%Y/%m/%d', default='logo/2018/09/24/infortx.png', verbose_name='head')
    name = models.CharField(max_length=20, verbose_name="昵称", null=True, blank=True)
    gender = models.SmallIntegerField(choices=set, verbose_name="性别", default=3)
    school = models.CharField(max_length=20, verbose_name="学校", null=True, blank=True)
    address = models.CharField(max_length=50, verbose_name="地址", null=True, blank=True)
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    home = models.CharField(max_length=30, verbose_name="故乡", null=True, blank=True)
    mobile = models.CharField(max_length=18, validators=[
        validators.RegexValidator(r'^1[3-9]\d{9}$', "手机号码格式错误")
    ], verbose_name="手机号或用户名")
    pwd = models.CharField(max_length=64, validators=[
        validators.MinLengthValidator(6)
    ], verbose_name="登录密码")

    class Meta:
        db_table = "person"


class SendImage(models.Model):
    head = models.ImageField(upload_to="imgs/%Y/%m/%d", verbose_name="图片")


