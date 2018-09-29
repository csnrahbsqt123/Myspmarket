from django.contrib import admin

# Register your models here.
from order.models import Order, Transport, Pay, OrderShops, UserAddress

admin.site.register(Order)
admin.site.register(Transport)
admin.site.register(Pay)
admin.site.register(OrderShops)
admin.site.register(UserAddress)
