from django.http import JsonResponse
import json
from .models import Sport
from .models import Item

def GetAllSport(request):
    if request.method=="GET":
        sport = list(Sport.objects.values())
        data = { i : sport[i] for i in range(0, len(sport)) }
        return JsonResponse(data)

def GetSport(request, *args, **kwargs):
    if request.method=="GET":
        sport_name = request.GET.get("name")
        # sport_name = kwargs['name']
        status =0
        message = ""
        if Sport.objects.filter(name=sport_name):
            status = 1
            message = "Sport Name Already Exits."
        else:
            status = 0
            message ="Sport Name Not Exits in Database."
        data ={
            'status':status,
            'message':message
        }
        return JsonResponse(data)
        

def GetAllItem(request, *args, **kwargs):
    if request.method=="GET":
        # sport = request.GET.get("name")
        sport_id = kwargs['sport_pk']
        print(sport_id)
        # sport = Sport.objects.get(id=sport_id)
        # data = list(Item.objects.filter(sport_type=sport).values())
        data = list(Sport.objects.values())
        return JsonResponse(data)

def Search(request, *arg, **kwargs):
    if request.method=="GET":
        item   =request.GET.get("item")
        brand  =request.GET.get("brand")
        quality=request.GET.get("quality")
        quantity=request.GET.get("quantity")
        sport  =request.GET.get("sport")

        id = Sport.objects.filter(name=sport).first()
        status =0
        message="Not Found"
        query =[]
        if sport and item and brand and quality:
            quantity = list(Item.objects.filter(name=item,brand=brand,quality=quality,sport_type=id).values())
            query = {i:quantity[i] for i in range(0,len(quantity))}
            status=1
            message="success"
        elif sport and item and brand:
            quality = list(Item.objects.filter(name=item,brand=brand,sport_type=id).values())
            query = {i:quality[i] for i in range(0,len(quality))}
            status=1
            message="success"
        elif sport and item:
            brands = list(Item.objects.filter(name=item,sport_type=id).values())
            query = {i:brands[i] for i in range(0,len(brands))}
            status=1
            message="success"
        elif sport:
            items =list(Sport.objects.filter(name=sport).first().item_set.values())
            query = { i : items[i] for i in range(0, len(items)) }
            status=1
            message="Success"
        # print(brand,quality,quantity,sport)
        # print(query)
        data ={
            'status':status,
            'message':message,
            'query':query,
        }
        return JsonResponse(data)