import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import OrderDetails,OrderItem,FoodMenu
from django.http import  HttpResponse
import csv
import json
import pandas as pd
# Create your views here.




def read_excel():
    xlx = pd.ExcelFile("Smartq Data708a203.xlsx")
    data1 = pd.read_excel(xlx, "food menu")
    for i in range(len(data1["itemname"])):
        FoodMenu.objects.create(itemname=data1["itemname"][i],availabletime = data1["availabletime"][i])
    data2 = pd.read_excel(xlx, "order details")
    for i in range(len(data2["orderid"])):
        obj = OrderDetails.objects.create(order_id = data2["orderid"][i],restaurant_id = data2["restaurantid"][i],
                                          billamount = data2["billamount"][i],timestamp = data2["timestamp"][i])
        list_of_order = eval(data2["orderedItems"][i])
        print(list_of_order)

        for i in list_of_order:
            order = OrderItem.objects.create(order_id = obj , itemname=i["itemname"],price = i["price"],
                                             quantity=i["quantity"])


class RestaurentsWiseSales(APIView):

    def post(self,request):
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            print(json_data)
        except Exception as e:
            json_data = request.POST.copy()
            print(e)

        my_date = datetime.datetime.strptime(json_data["date"], "%d-%m-%Y")
        list_of_data = OrderDetails.objects.filter( restaurant_id = json_data["restaurantid"],
                                                    timestamp__contains= my_date.date()).values_list("billamount",flat=True)
        print(sum(list_of_data))
        output= {"total_sales":sum(list_of_data)}

        return Response(output)




class SlotAvailable(APIView):
    def post(self,request):
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            print(json_data)
        except Exception as e:
            json_data = request.POST.copy()
            print(e)
        my_date = datetime.datetime.strptime(json_data["date"], "%d-%m-%Y")
        restaurantid = json_data["restaurantid"]
        list_of_data = OrderItem.objects.filter(order_id__restaurant_id=json_data["restaurantid"],
                                                   order_id__timestamp__contains=my_date.date()).order_by("-quantity")
        # print(list_of_data)
        breakfast = set()
        lunch  =  set()
        snacks = set()
        dinner = set()
        for i in list_of_data:

            food = FoodMenu.objects.get(itemname= i.itemname.lower())
            time_l = food.availabletime.split(",")
            time_l[0] = time_l[0].split("-")
            time_l[0][0] = float(time_l[0][0].replace(":",".").strip())
            time_l[0][1] = float(time_l[0][1].replace(":", ".").strip())
            time_l[1] = time_l[1].split("-")
            time_l[1][0] = float(time_l[1][0].replace(":", ".").strip())
            time_l[1][1] = float(time_l[1][1].replace(":", ".").strip())
            timesolt = {
                "break_fast": "07:00-11:00",
                "lunch": "12:30-15:30",
                "sancks": "16:30-19:00",
                "dinner": "19:30-23:00"
            }
            if time_l[0][0] <= 7.0 <= time_l[0][1] or time_l[1][0] <= 7.0 <= time_l[1][1] or time_l[0][0] <= 11.0 <= time_l[0][1] or time_l[1][0] <= 11.0 <= time_l[1][1]:
                breakfast.add(i.itemname)
            if time_l[0][0] <= 12.30 <= time_l[0][1] or time_l[1][0] <= 12.30 <= time_l[1][1] or time_l[0][0] <= 15.30 <= \
                    time_l[0][1] or time_l[1][0] <= 15.30 <= time_l[1][1]:
                lunch.add(i.itemname)
            if time_l[0][0] <= 16.30 <= time_l[0][1] or time_l[1][0] <= 16.30 <= time_l[1][1] or time_l[0][0] <= 19.00 <= \
                    time_l[0][1] or time_l[1][0] <= 19.00 <= time_l[1][1]:
                snacks.add(i.itemname)
            if time_l[0][0] <= 19.30 <= time_l[0][1] or time_l[1][0] <= 19.30 <= time_l[1][1] or time_l[0][0] <= 23.00 <= \
                    time_l[0][1] or time_l[1][0] <= 23.00 <= time_l[1][1]:
                dinner.add(i.itemname)
        print(breakfast)
        print(lunch)
        print(snacks)
        print(dinner)
        dicti = {}
        for i in breakfast:
            try:
                dicti[i] = dicti[i]+1
            except:
                dicti[i] = 0
        for i in lunch:
            try:
                dicti[i] = dicti[i]+1
            except:
                dicti[i] = 0
        for i in snacks:
            try:
                dicti[i] = dicti[i]+1
            except:
                dicti[i] = 0
        for i in dinner:
            try:
                dicti[i] = dicti[i]+1
            except:
                dicti[i] = 0

        day_slot = sorted((value,key) for (key,value) in dicti.items())
        print(day_slot)
        day_dict ={}
        for i in range(len(day_slot)):
            day_dict[day_slot[len(day_slot)-1-i][1]] = day_slot[len(day_slot)-1-i][0]

            if len(day_dict.values()) >=5:
                break

        print(len(day_dict.values()))

        output = {
            "top_5_most_sold_item_for_the_day":day_dict,
            "top_5_most_sold_item_per_slot":{
                "Breakfast":list(breakfast),
                "Lunch":list(lunch),
                "Snacks":list(snacks),
                "Dinner":list(dinner)
            }
        }
        return Response(output)


class ItemAvailable(APIView):
    def post(self,request):
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            print(json_data)
        except Exception as e:
            json_data = request.POST.copy()
            print(e)
        my_date = datetime.datetime.strptime(json_data["date"], "%d-%m-%Y")

        if FoodMenu.objects.filter(itemname = json_data["itemname"]).exists():
            list_of_item = OrderItem.objects.filter(order_id__timestamp__contains = my_date.date() ,
                                                    itemname__contains = json_data["itemname"]).values_list("quantity",flat=True)
            print(list_of_item)
            output ={"result":"Item Available","quantity_sold":sum(list_of_item)}
        else:
            print("hello")
            output = {"result":"Item not Available", "quantity_sold":0}
        return Response(output)

@csrf_exempt
@api_view(["GET","POST"])
def dumpOrder(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body.decode("utf-8"))
            print(json_data,"houu")
        except Exception as e:
            json_data = request.POST.copy()
            print(e)
        my_date = datetime.datetime.strptime(json_data["date"], "%d-%m-%Y")
        list_of_data = OrderItem.objects.filter(order_id__restaurant_id=json_data["restaurantid"],
                                                order_id__timestamp__contains=my_date.date())
        list_for_csv = []
        for i in list_of_data:
            dicti = {
                "Item Name":i.itemname,
                "Quantity":i.quantity,
                "Item Price":i.price,
                "Order Time":i.order_id.timestamp.strftime('%H:%M:%S')
            }
            list_for_csv.append(dicti)
        # print(list_for_csv)
        with open("abc.csv", "w") as infile:
            writer = csv.DictWriter(infile, fieldnames=list_for_csv[0].keys())
            writer.writeheader()
            for data in list_for_csv:
                writer.writerow(data)
        with open("abc.csv", 'rb') as infile:
            response = HttpResponse(infile, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=mylist.csv'
            return response
        # output = {"message": "Get request is not allowd"}
        # return HttpResponse(json.dumps(output))


    output ={"message":"Get request is not allowd"}
    return  HttpResponse(json.dumps(output))





def readData(request):
    read_excel()
    return HttpResponse("data is added")