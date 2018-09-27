from django import forms
from django.contrib.auth.models import User
from django.core import validators

from user.helper import set_password
from user.models import Person


class LoginForm(forms.ModelForm):
    # 登录modelform
    class Meta:
        model = Person
        fields = ["mobile", "pwd"]

        widgets = {
            "mobile": forms.TextInput(attrs={"class": "login-name", "placeholder": "请输入用户名/手机号"}),
            "pwd": forms.PasswordInput(attrs={"class": "login-password", "placeholder": "请输入密码"})
        }

        error_messages = {
            "mobile": {
                "required": "请输入手机号"
            },
            "pwd": {
                "required": "请输入密码"
            }
        }

    def clean(self):
        # 获取所有清洗后的数据
        clean_data = super(LoginForm, self).clean()
        # 获取得到的数据
        mobile = clean_data.get("mobile")
        pwd = clean_data.get("pwd")

        # 通过mobile验证,如果成功,验证密码
        data = Person.objects.filter(mobile=mobile).first()

        if data is None:
            # 不存在手机号
            raise forms.ValidationError({"mobile": "该手机号还未注册"})
        else:
            # 存在手机号,验证密码
            if set_password(pwd) == data.pwd:
                clean_data["data"] = data

                return clean_data
            else:
                raise forms.ValidationError({"pwd": "密码错误"})


class RegisterForm(forms.ModelForm):
    # 重复密码
    password = forms.CharField(max_length=32, min_length=6, error_messages={
        "max_length": "密码不能超过32个字符",
        "min_length": "密码不能少于6个字符",
        "required": "填写确认密码"},
                               widget=forms.PasswordInput(attrs={"class": "login-password",
                                                                 "placeholder": "请输入确认密码",
                                                                 "style": "margin:10px 18.75px 2px 18.75px"
                                                                 }),
                               )

    checkbox = forms.BooleanField(initial=0, error_messages={
        "required": "必须同意协议"
    })
    verify_code = forms.CharField(error_messages={
        "required": "请输入4位验证码"
    },
    )

    class Meta:
        model = Person
        fields = ["pwd", "mobile"]

        error_messages = {
            "pwd": {"max_length": "密码不能超过32个字符",
                    "min_length": "密码不能少于6个字符"},
            "mobile": {"required": "填写手机号"}
        }
        widgets = {
            "mobile": forms.TextInput(attrs={"class": "login-name",
                                             "placeholder": "请输入用户名/手机号",
                                             }),
            "pwd": forms.PasswordInput(attrs={"class": "login-password",
                                              "placeholder": "请输入密码",
                                              "style": "margin:10px 18.75px 2px 18.75px"
                                              })
        }

    # 验证验证码是否正确
    def clean_verify_code(self):
        # 获取输入的验证码
        data = self.cleaned_data.get("verify_code")
        # 获取session中的验证码
        session_code = self.data.get("session_code")
        if data != session_code:
            raise forms.ValidationError("验证码错误")
        else:
            return data

    # 验证手机号是否被注册
    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")
        data = Person.objects.filter(mobile=mobile).exists()
        if data:
            raise forms.ValidationError("该手机号码已被注册")
        else:
            return mobile

    # 验证验证码是否正确
    # def clean_verify_code(self):
    #     verify_code=self.cleaned_data.get("verify_code")

    # 验证两次密码是否相同
    def clean(self):
        data = super(RegisterForm, self).clean()
        pwd1 = data.get("pwd")  # 输入密码
        pwd2 = data.get("password")  # 验证密码
        if pwd1 and pwd2 and pwd1 != pwd2:
            raise forms.ValidationError({"password": "两次密码不一致,请重新输入"})
        else:
            if pwd1:
                data["pwd"] = set_password(pwd1)
                return data


# 个人资料modleform
class PersonModelsForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["name", "birthday", "school", "home", "address", "mobile","gender","head"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "infor-tele", "placeholder": "昵称"}),
            "birthday": forms.TextInput(attrs={"class": "infor-tele", "placeholder": "生日"}),
            "gender": forms.RadioSelect(),
            "school": forms.TextInput(attrs={"class": "infor-tele", "placeholder": "学校"}),
            "address": forms.TextInput(attrs={"class": "infor-tele", "placeholder": "家庭地址"}),
            "mobile": forms.TextInput(attrs={"class": "infor-tele", "placeholder": "手机号"}),
            "home": forms.TextInput(attrs={"class": "infor-tele", "placeholder": "家乡"}),
        }
