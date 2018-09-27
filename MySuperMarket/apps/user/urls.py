from django.conf.urls import url

from user.views import LoginView, index, RegisterView, ForgetView, PersonCenterView, PersonView, AddressView, \
    SendVerifyCode

urlpatterns=[
    url(r'^login/$',LoginView.as_view(),name="login"),
    url(r'^index/$',index,name="index"),
    url(r'^register/$',RegisterView.as_view(),name="register"),
    url(r'^forget/$',ForgetView.as_view(),name="forget"),
    url(r'^center/$',PersonCenterView.as_view(),name="person_center"),
    url(r'^person/$',PersonView.as_view(),name="person"),
    url(r'^address/$',AddressView.as_view(),name="g_address"),
    url(r'^send/$',SendVerifyCode.as_view(),name="send"),
]