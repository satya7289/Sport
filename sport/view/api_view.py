from django.http import JsonResponse

from sport.models import Sport
from sport.models import Item
from sport.models import Checkout


def GetAllSport(request):
    if request.method == "GET":
        sport = list(Sport.objects.values())
        data = {i: sport[i] for i in range(0, len(sport))}
        return JsonResponse(data)


def GetSport(request, *args, **kwargs):
    if request.method == "GET":
        sport_name = request.GET.get("name")
        # sport_name = kwargs['name']
        status = 0
        message = ""
        if Sport.objects.filter(name=sport_name):
            status = 1
            message = "Sport Name Already Exits."
        else:
            status = 0
            message = "Sport Name Not Exits in Database."
        data = {
            'status': status,
            'message': message
        }
        return JsonResponse(data)


def GetAllItem(request, *args, **kwargs):
    if request.method == "GET":
        # sport = request.GET.get("name")
        sport_id = kwargs['sport_pk']
        print(sport_id)
        # sport = Sport.objects.get(id=sport_id)
        # data = list(Item.objects.filter(sport_type=sport).values())
        data = list(Sport.objects.values())
        return JsonResponse(data)


def Search(request, *arg, **kwargs):
    if request.method == "GET":
        r_item = request.GET.get("item")
        r_brand = request.GET.get("brand")
        r_quality = request.GET.get("quality")
        r_sport = request.GET.get("sport")

        status = 0
        message = "Not Found"
        # id = Sport.objects.filter(name=sport).first()
        try:
            sport = Sport.objects.get(name=r_sport)
            query = []
            if sport and r_item and r_brand and r_quality:
                item = Item.objects.filter(sport_type=sport, name=r_item, brand=r_brand,
                                           quality=r_quality, available__gte=0).first()
                types = item.available
                message = "success"
                status = 1
            elif sport and r_item and r_brand:
                items = Item.objects.filter(sport_type=sport, name=r_item, brand=r_brand,
                                            available__gte=0)
                types = []
                for item in items:
                    if item.quality not in types:
                        types.append(item.quality)
                message = "success"
                status = 1

            elif sport and r_item:
                items = Item.objects.filter(name=r_item, sport_type=sport, available__gte=0)
                types = []
                for item in items:
                    if item.brand not in types:
                        types.append(item.brand)
                message = "success"
                status = 1
            elif sport:
                items = sport.item_set.filter(available__gte=0)
                types = []
                for item in items:
                    if item.name not in types:
                        types.append(item.name)
                message = "success"
                status = 1
                # query =Item.objects.filter(name=types[0],available__gte=0).values().first()
            data = {
                'status': status,
                'message': message,
                'query': query,
                'types': types,
            }
            return JsonResponse(data)
        except:
            data = {
                'status': status,
                'message': message,
            }
            return JsonResponse(data)


def CheckoutDetail(request):
    if request.method == "GET":
        id = request.GET.get("id")
        status = 0
        message = "Not Found"
        query = []
        if id:
            checkout = Checkout.objects.filter(id=id).first()
            if checkout:
                total_items = checkout.item_list.count()
                items = list(checkout.item_list.values())
                items = {i: items[i] for i in range(0, len(items))}
                first_name = checkout.student_name.first_name
                last_name = checkout.student_name.last_name
                roll_no = checkout.student_name.roll_no
                email = checkout.student_name.email
                sport = checkout.student_name.team.first().name
                remarks = ""
                try:
                    remarks = checkout.checkin.remarks
                except:
                    remarks = ""
                query = {
                    'total_items': total_items,
                    'items': items,
                    'first_name': first_name,
                    'last_name': last_name,
                    'roll_no': roll_no,
                    'email': email,
                    'sport': sport,
                    'remarks': remarks,
                }
                # print(checkout,items,first_name,last_name,email,sport,roll_no)
                status = 1
                message = "success"
        data = {
            'status': status,
            'message': message,
            'query': query
        }
        return JsonResponse(data)
