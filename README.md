# SmartQi
This is a Food order Management app . This will give Restaurant wise sales . It also give information about particular requested item available currently. And further, for the provided date how many items are sold.Also provide facilities of Dump all the orders of a day of a restaurant into a csv file
Instruction for running
1. Create a virtual environment with python version >= 3.5
2. run command pip install -r requirments.txt by visting the game_listing app
3. run the app using python manage.py runserver command
4. It uses token authentication for api:
so use token given below:
Put this in Authorization header:
Token 1192966f51bb44a2c4f47c14b4572627ca9191f2
or create new token from admin panel by creating user default user id and pass is :
userid = m
pass = m
5.For getting Restaurant wise sales make the POST request on 
` http://127.0.0.1:8000/api/rest_wise_sale/`
## Request body :
    `{
    "restaurantid":"tuckshop",
    "date":"21-10-2019"
    }`
## Response :
    `{
    "total_sales": 1400
    }`
6.For getting ​ Is a particular requested item available currently. And further, for the provided date how many items are sold.
`http://127.0.0.1:8000/api/​ item_available​ /`
## Request body :
    `{
    "itemname":"idli",
    "date":"21-10-2019"
    }`
## Response :
    `{
    "result": "Item Available",
    "quantity_sold": 34
    }`
7. Get List by Time slot
List out top 5 most ordered/ trending items for a given restaurant
- of the day
- per slots
`http://127.0.0.1:8000/api/slot /`
## Request body :
    `{
    "restaurantid":"tuckshop",
    "date": "21-10-2019"
    }`
## Response :
    `{
    "top_5_most_sold_item_for_the_day": {
    "set dosa": 2,
    "rava idli": 2,
    "puttu": 2,
    "pongal": 2,
    "ghee dosa": 2
    },
    "top_5_most_sold_item_per_slot": {
    "Breakfast": [
    "rava idli",
    "ghee dosa",
    "set dosa",
    "pongal",
    "puttu"
    ],
    "Lunch": [],
    "Snacks": [
    "rava idli",
    "ghee dosa",
    "set dosa",
    "pongal",
    "puttu"
    ],
    "Dinner": [
    "rava idli",
    "ghee dosa",
    "set dosa",
    "pongal",
    "puttu"
    ]
    }}`
8. For Dump all the orders of a day of a restaurant into a csv file
` http://127.0.0.1:8000/api/dump_order/`
## Request body :
    `{
    "restaurantid":"tuckshop",
    "date":"21-10-2019"
    }`
## Response : The csv file will be downloaded
