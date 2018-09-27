from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

# 购物车
from django_redis import get_redis_connection

from goods.models import GoodsSKU


class ShopCartView(View):
    def get(self, request):
        return render(request, "cart/shopcart.html")

    def post(self, request):
        """
        思路分析:
        1.需要通过ajax传入参数sku_id(商品id),count(商品数量)
        2.验证传入的参数是否正确
        3.验证商品是否存在
        4.验证用户是否登陆
        5.验证库存是否足够
        56.保存到redis中
        :param request:
        :return:
        """
        # 获取传入的参数
        sku_id = request.POST.get("sku_id")
        count = request.POST.get("count")
        # 验证参数是否是整数
        try:
            sku_id = int(sku_id)
            count = int(count)
        except:
            return JsonResponse({"error": 1, "msg": "参数不正确"})

        # 验证商品是否存在

        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({"error": 2, "msg": "商品不存在"})

        # 验证用户是否登陆,如果没有登录通过ajax的js返回一条数据
        user_id = request.session.get("id")
        if user_id is None:
            """用户未登陆"""
            return JsonResponse({"error": 3, "msg": "用户还未登陆,请登录!!"})
        # 验证库存是否足够
        if sku.stock < count:
            """库存不足"""
            return JsonResponse({"error": 4, "msg": "商品库存不足"})

        # 保存到redis中
        # 默认配置到redis中
        cnn = get_redis_connection("default")
        # 使用连接上的方法操作redis
        # cnn.hset('对象名'，'属性' ，'值')
        cart_key="cart_%s" % user_id
        cnn.hincrby(cart_key, sku_id, count)

        total_count = 0
        vars = cnn.hvals(cart_key)
        if len(vars) > 0:
            for v in vars:
                total_count += int(v)

        return JsonResponse({"error":0,"msg":"添加成功","total_count":total_count})

# 结算
class AccountView(View):
    def get(self, request):
        return render(request, "cart/tureorder.html")

    def post(self, request):
        return render(request, "cart/tureorder.html")
