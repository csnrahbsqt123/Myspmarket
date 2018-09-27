"""MySuperMarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.decorators.cache import cache_page

from goods.views import IndexView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^supermarket/', include("user.urls", namespace="supermarket")),
    url(r'^supermarket/', include("goods.urls", namespace="goods")),
    url(r'^ckeditor/', include("ckeditor_uploader.urls")),
    url(r'^$', IndexView.as_view()),
    url(r'^shopCart/', include("cart.urls",namespace="shopCart")),
    # 全文搜索框架
    url(r'^search/', include('haystack.urls')),
]