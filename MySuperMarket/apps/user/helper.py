import hashlib
import sys
# from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
# # from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
# from aliyunsdkcore.client import AcsClient
# # import uuid
# from aliyunsdkcore.profile import region_provider
# # from aliyunsdkcore.http import method_type as MT
# # from aliyunsdkcore.http import format_type as FT
from django.conf import settings

#登录验证器
from django.shortcuts import redirect
from django.urls import reverse

from user.models import Person


def verify_login_required(func):
    """
    :param func: 传入的函数
    :return:
    """    # 登陆验证器
    def verify(request, *args, **kwargs):
        # 判断session中是否有ID,如果没有说明没有登录，请登录
        if request.session.get("id") is None:
            # 配置文件中获取登录的URL地址
            # login_url = settings.LOGIN_URL
            return redirect(reverse("supermarket:login"))
        else:
            # 返回被调用函数
            return func(request, *args, **kwargs)
    return verify


def set_password(pwd):
    #密码加密
    key=settings.SECRET_KEY
    pwd=key+str(pwd)
    h=hashlib.sha1(pwd.encode("utf-8"))
    h=h.hexdigest()
    return h


def verify_mobile_pwd(mobile,pwd):
    #手机与密码验证

    return Person.objects.filter(mobile=mobile,pwd=set_password(pwd)).first()




# # 注意：不要更改
# REGION = "cn-hangzhou"
# PRODUCT_NAME = "Dysmsapi"
# DOMAIN = "dysmsapi.aliyuncs.com"
#
# acs_client = AcsClient(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET, REGION)
# region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)
#
#
# def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
#     smsRequest = SendSmsRequest.SendSmsRequest()
#     # 申请的短信模板编码,必填
#     smsRequest.set_TemplateCode(template_code)
#
#     # 短信模板变量参数
#     if template_param is not None:
#         smsRequest.set_TemplateParam(template_param)
#
#     # 设置业务请求流水号，必填。
#     smsRequest.set_OutId(business_id)
#
#     # 短信签名
#     smsRequest.set_SignName(sign_name)
#
#     # 数据提交方式
#     # smsRequest.set_method(MT.POST)
#
#     # 数据提交格式
#     # smsRequest.set_accept_format(FT.JSON)
#
#     # 短信发送的号码列表，必填。
#     smsRequest.set_PhoneNumbers(phone_numbers)
#
#     # 调用短信发送接口，返回json
#     smsResponse = acs_client.do_action_with_exception(smsRequest)
#
#     # TODO 业务处理
#
#     return smsResponse