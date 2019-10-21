from django.http import JsonResponse
import json
from .models import Sport
from .models import Item

def GetAllSport(request):
    if request.method=="GET":
        sport = list(Sport.objects.values())
        data = { i : sport[i] for i in range(0, len(sport)) }
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