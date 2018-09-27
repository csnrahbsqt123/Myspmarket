from django.conf.urls import url

from cart.views import ShopCartView, AccountView

urlpatterns = [
    url(r'^$', ShopCartView.as_view(), name="cart"),
    url(r'^tureorder/$', AccountView.as_view(), name="tureorder"),
]
