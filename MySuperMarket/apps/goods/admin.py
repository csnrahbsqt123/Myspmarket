from django.contrib import admin

# Register your models here.
from goods.models import Category, Unit, GoodsSPU, GoodsSKU, Photo, Banner, ActivityZone, ActivityZoneGoods, Activity

admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(GoodsSPU)
admin.site.register(GoodsSKU)
admin.site.register(Photo)
admin.site.register(Banner)
admin.site.register(ActivityZone)
admin.site.register(ActivityZoneGoods)
admin.site.register(Activity)



