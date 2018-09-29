from django.core import validators
from django.db import models

# Create your models here.

# 收货地址
from db.base_model import BaseModel


class UserAddress(BaseModel):
    user = models.ForeignKey(to="user.Person", verbose_name="用户id")
    take_goods_name = models.CharField(max_length=20, verbose_name="收货人姓名")
    mobile = models.CharField(max_length=12, verbose_name="收货人电话",validators=[
        validators.RegexValidator(r'^1[3-9]\d{9}$',"手机格式错误")
    ])
    hcity = models.CharField(verbose_name="省id", max_length=100)
    hproper = models.CharField(verbose_name="市id", max_length=100,blank=True, default='')
    harea = models.CharField(verbose_name="区id", max_length=100,blank=True, default='')
    describe = models.CharField(verbose_name="详细描述", max_length=255)
    is_default_address = models.BooleanField(default=False, verbose_name="是否默认地址",blank=True)

    class Meta:
        verbose_name = "收货地址管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.take_goods_name


class Order(BaseModel):
    # 订单状态
    status = (
        (0, "待发货"),
        (1, "待收货"),
        (2, "待评价"),
        (3, "退换货"),
        (4, "已完成"),
    )
    order_num = models.CharField(max_length=20, verbose_name="订单编号")
    order_price = models.DecimalField(verbose_name="订单金额", max_digits=9, decimal_places=2, default=0)
    user_id = models.ForeignKey(to="user.Person", verbose_name="用户id")
    take_goods_name = models.CharField(max_length=20, verbose_name="收货人姓名")
    mobile = models.CharField(max_length=12, verbose_name="收货人电话")
    address = models.CharField(verbose_name="收货人地址", max_length=200)
    order_status = models.SmallIntegerField(choices=status, verbose_name="订单状态")
    transport = models.ForeignKey(to="Transport", verbose_name="运输方式")
    transport_price = models.DecimalField(verbose_name="运费", max_digits=9, decimal_places=2, default=0)
    pay = models.ForeignKey(to="Pay", verbose_name="付款方式")
    actual_amount = models.DecimalField(verbose_name="实付金额", max_digits=9, decimal_places=2, default=0)

    class Meta:
        verbose_name = "订单管理"
        verbose_name_plural = verbose_name


# 运输方式
class Transport(BaseModel):
    name = models.CharField(max_length=20, verbose_name="运输方式名称")
    price = models.DecimalField(verbose_name="价格", max_digits=9, decimal_places=2, default=0)

    class Meta:
        verbose_name = "运输方式"
        verbose_name_plural = verbose_name


class Pay(BaseModel):
    pay_name = models.CharField(max_length=20, verbose_name="支付名称")
    img = models.ImageField(upload_to="pay/%Y/%m/%d", verbose_name="图片")

    class Meta:
        verbose_name = "支付方式"
        verbose_name_plural = verbose_name


# 订单商品信息
class OrderShops(models.Model):
    order_id = models.ForeignKey(to="Order", )
    goods_sku = models.ForeignKey(to="goods.GoodsSKU", verbose_name="商品id")
    num = models.IntegerField(verbose_name="商品数量")
    price = models.DecimalField(verbose_name="商品价格",max_digits=9,decimal_places=2,default=0)
