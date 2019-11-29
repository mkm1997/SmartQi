from django.contrib import admin
from .models import OrderItem, OrderDetails,FoodMenu

# Register your models here.
admin.site.register(OrderDetails)
admin.site.register(OrderItem)
admin.site.register(FoodMenu)




