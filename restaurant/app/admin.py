from django.contrib import admin
from .models import Profile, SubItem,Item,Table,Order,SubOrder,OrderItem,Feedback,Action,Payment,Equipment
# Register your models here.

admin.site.register(Profile)
admin.site.register(Item)
admin.site.register(SubItem)
admin.site.register(Table)
admin.site.register(Order)
admin.site.register(SubOrder)
admin.site.register(OrderItem)
admin.site.register(Feedback)
admin.site.register(Action)
admin.site.register(Payment)
admin.site.register(Equipment)