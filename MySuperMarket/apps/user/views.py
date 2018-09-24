import uuid

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django.views import View

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
            # request.session.clear()
            request.session["id"] = data.id
            request.session["mobile"] = data.mobile
            request.session.set_expiry(0)
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
        data = request.POST
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
        return render(request, "user/member.html", {"mobile": mobile})


# 个人资料
class PersonView(BaseVerifyView):
    def post(self, request):
        return render(request, "user/infor.html")

    def get(self, request):
        id = request.session.get("id")
        user = Person.objects.filter(id=id).first()
        form = PersonModelsForm(instance=user)
        return render(request, "user/infor.html", {"form": form})


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
            return JsonResponse({"status": 400, "mag": "该号码已经被注册"})

        # 验证号码是否已经注册
        res = Person.objects.filter(mobile=phone).exists()
        if res:
            return JsonResponse({"status": 400, "mag": "该号码已经被注册"})

        # 生成随机验证码
        import random
        code = [str(random.randint(0, 9)) for i in range(4)]
        code = "".join(code)
        print("==============" + code + "=============")

        __business_id = uuid.uuid1()
        # print(__business_id)
        params = "{\"code\":\"%s\"}" % code
        rs = send_sms(__business_id, phone, "尹强", "SMS_141905190", params)
        print(rs)

        # 将验证码保存到session中,
        request.session["verify_code"] = code
        request.session.set_expiry(60)

        return JsonResponse({"status": 200})
