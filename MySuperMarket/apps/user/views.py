import uuid

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django.views import View
from django.views.decorators.csrf import csrf_exempt

from db.base_view import BaseVerifyView
from user.forms import LoginForm, RegisterForm, PersonModelsForm
from user.models import Person


def index(request):
    # 首页
    return render(request, "index/index.html")


# 登录
class LoginView(View):
    def post(self, request):
        data = request.POST
        form = LoginForm(data)
        if form.is_valid():
            # 如果验证成功,则将用户名及密码传到session中
            data = form.cleaned_data.get("data")
            request.session.clear()
            request.session["id"] = data.id
            request.session["mobile"] = data.mobile
            request.session.set_expiry(0)

            if request.GET.get("next"):
                return redirect(request.GET.get("next"))
            else:
                return redirect(reverse("supermarket:person_center"))

        else:
            content = {
                "form": form,
            }
            return render(request, "user/login.html", content)

    def get(self, request):
        login_form = LoginForm()
        return render(request, "user/login.html", {"form": login_form})


# 注册
class RegisterView(View):
    def post(self, request):
        # 接收数据
        session_code = request.session.get("session_code")
        # 强制转换为字典
        data = request.POST.dict()
        data["session_code"] = session_code
        verify_form = RegisterForm(data)
        # 获取session中的验证码

        if verify_form.is_valid():
            # 验证通过
            verify_form.save()
            return redirect(reverse("supermarket:login"))
        else:
            # 验证失败
            return render(request, "user/reg.html", {"verify_form": verify_form})

    def get(self, request):
        verify_form = RegisterForm()
        return render(request, "user/reg.html", {"verify_form": verify_form})


# 忘记密码
class ForgetView(View):
    def post(self, request):
        return render(request, "user/forgetpassword.html")

    def get(self, request):
        return render(request, "user/forgetpassword.html")


# 个人中心
class PersonCenterView(BaseVerifyView):
    def post(self, request):
        # return render(request,"user/member.html")
        pass

    def get(self, request):
        mobile = request.session.get("mobile")
        user_id = request.session.get("id")
        person = Person.objects.get(id=user_id)
        content = {
            "mobile": mobile,
            "person": person,

        }
        return render(request, "user/member.html", content)


# 个人资料
class PersonView(BaseVerifyView):
    def post(self, request):
        # 获取id
        id=request.session.get("id")


        # 需要修改当前登陆人这个对象
        user = Person.objects.filter(pk=id).first()
        # form 保持数据的 需要传第二个参数 instance = 需要修改的实例对象
        form = PersonModelsForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse('supermarket:person_center'))
        else:
            return render(request, "user/infor.html", {"form": form})

    # user_id = request.session.get("id")
    # data = request.POST
    # file = request.FILES["head"]
    # person = Person.objects.get(id=user_id)
    # person.head = file
    # person.save()
    # form = PersonModelsForm(data)
    # if form.is_valid():
    #     res = form.cleaned_data
    #     Person.objects.filter(id=user_id).update(name=res.get("name"),
    #                                              birthday=res.get("birthday"),
    #                                              school=res.get("school"),
    #                                              home=res.get("home"),
    #                                              address=res.get("address"),
    #
    #                                              )
    #
    #     return render(request, "user/member.html")

    def get(self, request):
        id = request.session.get("id")
        user = Person.objects.filter(id=id).first()
        form = PersonModelsForm(instance=user)
        content = {
            "form": form,
            "user": user
        }
        return render(request, "user/infor.html", content)


# 单独写一个图片上传
# @csrf_exempt  # 移除令牌限制
# def unload(request):
#     if request.method == "POST":
#         id = request.session.get("id")
#         # 获取对象
#         person = Person.objects.get(id=id)
#         # 保存图片
#         person.head = request.FILES["file"]
#         person.save()
#         return JsonResponse({"error": 0})
#     else:
#         return JsonResponse({"error": 1})


# 收货地址
class AddressView(View):
    def post(self, request):
        return render(request, "user/gladdress.html")

    def get(self, request):
        return render(request, "user/gladdress.html")


class SendVerifyCode(View):
    def post(self, request):
        phone = request.POST.get("tel", "0")

        # 验证手机格式
        import re
        r = re.compile(r"^1[3-9]\d{9}$")
        res = re.search(r, phone)

        if res is None:
            return JsonResponse({"status": 400, "msg": "手机格式不正确"})

        # 验证号码是否已经注册
        res = Person.objects.filter(mobile=phone).exists()
        if res:
            return JsonResponse({"status": 400, "msg": "该号码已经被注册"})

        # 生成随机验证码
        import random
        code = [str(random.randint(0, 9)) for i in range(4)]
        code = "".join(code)
        print("==============" + code + "=============")
        # 将验证码保存到session中,
        request.session["session_code"] = code
        request.session.set_expiry(60)
        # __business_id = uuid.uuid1()
        # print(__business_id)
        # params = "{\"code\":\"%s\"}" % code
        # rs = send_sms(__business_id, phone, "尹强", "SMS_141905190", params)
        return JsonResponse({"status": 200})
