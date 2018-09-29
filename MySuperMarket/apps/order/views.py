from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from django_redis import get_redis_connection

from db.base_view import BaseVerifyView
from goods.models import GoodsSKU
from order.forms import AddressForm
from order.models import Transport, UserAddress

"""确认订单"""


class ConfirmOderView(BaseVerifyView):
    def get(self, request):
        # 获取用户id
        user_id = request.session.get("id")
        # 获取提交过来的商品id
        shop_list = request.GET.getlist("my_shop")
        goods_list = []
        """数量保存在redis中"""
        cnn = get_redis_connection("default")
        cart_key = "cart_%s" % user_id

        # 总价
        total_price = 0
        for val in shop_list:
            goods = GoodsSKU.objects.get(id=val)
            # 获取redis中的数量(count)
            count = cnn.hget(cart_key, val)
            count = int(count)
            # 添加一个count属性
            goods.count = count
            price = goods.price
            total_price += price * count
            goods_list.append(goods)

        # 获取所有运输方式
        transport = Transport.objects.filter(is_delete=False).order_by("price")
        my_transport = transport.first()

        # 计算支付总金额
        total_price_trans = total_price + my_transport.price

        # 获取为默认地址的信息
        address = UserAddress.objects.filter(is_delete=False, is_default_address=True).first()

        content = {
            "goods_list": goods_list,
            "total_price": total_price,
            "total_price_trans": total_price_trans,
            "transport": transport,
            "address": address
        }

        return render(request, "order/tureorder.html", content)


"""全部订单"""


class AllOrderView(BaseVerifyView):
    def get(self, request):
        return render(request, "order/allorder.html")


"""新增收货地址"""


class AddAddressView(BaseVerifyView):
    def post(self, request):
        """
        验证表单并保存到表中
        通过Ajax请求来验证
        :param request:
        :return:
        """
        data = request.POST.dict()
        form = AddressForm(data)
        if form.is_valid():
            form.instance.user_id = request.session.get("id")
            form.save()
            return JsonResponse({"ok": 0})
        else:
            return JsonResponse({"ok": 1, "error": form.errors})

    def get(self, request):
        form = AddressForm()
        return render(request, "order/address.html", {"form": form})


"""收货地址列表"""


class AddressListView(BaseVerifyView):
    def post(self, request):
        return render(request, "order/village.html")

    def get(self, request):
        return render(request, "order/village.html")


"""提交订单"""


class SubmitOrderView(BaseVerifyView):
    def post(self, request):

        return render(request, "order/order.html")

    def get(self, request):
        return render(request, "order/order.html")
