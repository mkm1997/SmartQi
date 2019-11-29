from django.urls import re_path,include
from . import views

urlpatterns = [

    re_path(r'^read_data/' , views.readData ,name= "readData"),
    re_path(r'^rest_wise_sale/',views.RestaurentsWiseSales.as_view() , name="rest_wise_sales"),
    re_path(r'^item_available/', views.ItemAvailable.as_view() , name='item-available'),
    re_path(r'^slot/',views.SlotAvailable.as_view(), name= "slot-available"),
    re_path(r'^dump_order/',views.dumpOrder , name="dump_order")

]
