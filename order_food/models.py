from django.db import models

# Create your models here.


class FoodMenu(models.Model):
    itemname = models.CharField(max_length=2000)
    availabletime = models.CharField(max_length=2000)
    def __str__(self):
        return self.availabletime



class OrderDetails(models.Model):
    order_id = models.CharField(max_length=2000,unique=True)
    restaurant_id = models.CharField(max_length=200)
    billamount = models.IntegerField()
    timestamp = models.DateTimeField()
    def __str__(self):
        return self.restaurant_id

class OrderItem(models.Model):
    order_id = models.ForeignKey(OrderDetails,on_delete=models.CASCADE)
    itemname = models.CharField(max_length=2000)
    quantity = models.IntegerField()
    price = models.IntegerField()
    def __str__(self):
        return self.itemname


