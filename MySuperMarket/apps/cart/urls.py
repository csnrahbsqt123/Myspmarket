from django.conf.urls import url

from cart.views import  AccountView, CartReduceView, CartView, ShopAddView

urlpatterns = [
    url(r'^add/$', ShopAddView.as_view(), name="add"),
    url(r'^$', CartView.as_view(), name="cart"),
    url(r'^tureorder/$', AccountView.as_view(), name="tureorder"),
    url(r'^reduce/$', CartReduceView.as_view(), name="reduce"),
]
