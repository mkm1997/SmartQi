from rest_framework.serializers import ModelSerializer,Serializer
from .models import OrderItem , OrderDetails,FoodMenu

class OrderItemSerializers(ModelSerializer):
    class Meta:
        model = OrderItem

        fields = '__all__'


class OrderDetailsSerializers(ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = '__all__'

class FoodMenuSerializers(ModelSerializer):
    class Meta:
        model = FoodMenu
        fields = '__all__'