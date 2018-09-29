from django.conf.urls import url

from order.views import ConfirmOderView, AllOrderView, AddAddressView, SubmitOrderView, AddressListView

urlpatterns=[
    url(r'^$',ConfirmOderView.as_view(),name="确认订单"),
    url(r'^all_order/$',AllOrderView.as_view(),name="全部订单"),
    url(r'^add_address/$',AddAddressView.as_view(),name="新增地址"),
    url(r'^submit/$',SubmitOrderView.as_view(),name="提交订单"),
    url(r'^address_list/$',AddressListView.as_view(),name="地址列表"),
]