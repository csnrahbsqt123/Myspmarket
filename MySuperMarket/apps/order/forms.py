from django import forms
from django.core import validators

from order.models import UserAddress


class AddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        exclude = ["update_time", "create_time", "is_delete", "user"]
        error_messages = {
            "take_goods_name": {
                "required": "收货人姓名必填"
            },
            "mobile": {
                "required": "收货人联系电话必填"
            },
            "hcity": {
                "required": "地址必填"
            },
            "hproper": {
                "required": "地址必填"
            },
            "harea": {
                "required": "地址必填"
            },
            "describe": {
                "required": "详细地址必填"
            }
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['mobile'].validators.append(validators.RegexValidator(r'^1[3-9]\d{9}$', "手机格式错误"))
