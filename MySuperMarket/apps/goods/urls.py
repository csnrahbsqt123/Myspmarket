from django.conf.urls import url

from goods.views import CategoryView, DetailView, IndexView

urlpatterns=[
    url(r'^category/(?P<cate_id>\d+)_(?P<order>\d).html/$',CategoryView.as_view(),name="category"),
    url(r'^detail/(?P<sku_id>\d+)/$',DetailView.as_view(),name="detail"),
    url(r'^$',IndexView.as_view(),name="index")
]