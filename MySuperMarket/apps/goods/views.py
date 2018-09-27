from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection

from goods.models import Category, GoodsSPU, GoodsSKU, Banner, ActivityZone, Activity


class IndexView(View):
    def get(self, request):
        # 首页轮播图处理
        banners = Banner.objects.filter(is_delete=False).order_by("order")
        # 活动管理
        active = Activity.objects.filter(is_delete=False)

        # 活动专区
        activityzones = ActivityZone.objects.filter(is_delete=False, is_on_sale=1).order_by("order")

        content = {
            "banners": banners,
            "activityzones": activityzones,
            "active": active,

        }

        return render(request, "goods/index.html", content)


class CategoryView(View):
    """
    分类
    """

    def get(self, request, cate_id=0, order=0):
        cate_id = int(cate_id)
        order = int(order)
        # 获取所有分类
        categorys = Category.objects.filter(is_delete=False)
        # 当cate_id不等于0,就查出对应分类下的所有商品

        if cate_id == 0:
            category = categorys.first()
        else:
            category = Category.objects.get(id=cate_id)

        # 获取当前分类下的所有商品
        goodslist = category.goodssku_set.all()

        total_count = 0
        if request.session.get("id"):
            cnn = get_redis_connection('default')
            cart_key = "cart_%s" % request.session.get("id")
            vars = cnn.hvals(cart_key)
            if len(vars) > 0:
                for v in vars:
                    total_count += int(v)

        # 创建一个排序规则
        rule = ["id", "sale_num", "-price", "price", "-create_time"]
        currt = rule[order]

        goodslist = goodslist.order_by(currt)

        content = {
            "categorys": categorys,
            "cate_id": cate_id,
            "goodlist": goodslist,
            "order": order,
            "total_count": total_count,
        }
        return render(request, "goods/category.html", content)


class DetailView(View):
    def get(self, request, sku_id):
        sku_id = int(sku_id)
        goodspu = GoodsSKU.objects.get(id=sku_id)
        content = {
            "goodspu": goodspu
        }
        return render(request, "goods/detail.html", content)
