import datetime as D
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import Http404

from sport.models import Item
from sport.models import ListOfItem
from sport.models import Checkin
from sport.models import Checkout


class CheckinListView(View):
    template_name = "checkin/CheckinList.html"

    def get(self, request):
        if request.method == "GET":
            checkin_list = Checkout.objects.filter(checkin_status=False)
        return render(request, self.template_name, {"checkins": checkin_list})


class CheckinDetailView(View):
    template_name = "checkin/CheckinDetail.html"

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            checkout_id = kwargs["checkout_pk"]
            try:
                checkout = Checkout.objects.get(id=checkout_id)
                return render(request, self.template_name, {"checkout": checkout})

            except Checkout.DoesNotExist:
                raise Http404


class CheckinView(View):
    def post(self, request, *arg, **kwargs):
        if request.method == "POST":
            checkout_id = request.POST.get("checkout-id")
            checkout = Checkout.objects.get(id=checkout_id)
            if not checkout.checkin_status:
                item_list = checkout.item_list.all()
                checkin_status_count = 0
                checkout_item_list_count = checkout.item_list.count()
                remarks = ""
                remarks += str(D.datetime.now())
                remarks += "<br>"
                list_of_items = []
                for i, checkout_item in enumerate(item_list):
                    item_id = request.POST.get("form-item-id-" + str(i + 1))
                    quality = request.POST.get("form-item-quality-" + str(i + 1))
                    quantity = request.POST.get("form-item-quantity-" + str(i + 1))

                    item = Item.objects.get(id=item_id)
                    prev_name = item.name
                    prev_brand = item.brand
                    prev_quality = item.quality
                    prev_sport_type = item.sport_type

                    if quality != prev_quality:
                        try:
                            check_item = Item.objects.filter(
                                sport_type=prev_sport_type,
                                name=prev_name,
                                brand=prev_brand,
                                quality=quality,
                            ).first()
                            if quality == "Lost":
                                check_item.quantity += int(quantity)
                            else:
                                check_item.available += int(quantity)
                                check_item.quantity += int(quantity)
                            check_item.save()
                        except:
                            if quality == "Lost":
                                available = 0
                            else:
                                available = int(quantity)
                            new_item = Item(
                                name=prev_name,
                                brand=prev_brand,
                                quantity=quantity,
                                available=available,
                                quality=quality,
                                sport_type=prev_sport_type,
                                created_at=D.datetime.now().date(),
                            )
                            new_item.save()
                    else:
                        item.available += int(quantity)
                        item.save()

                    if checkout_item.item_quantity > int(quantity):
                        checkout_item.item_quantity -= int(quantity)
                        checkout_item.save()

                    elif checkout_item.item_quantity == int(quantity):
                        checkin_status_count += 1
                        checkout.item_list.remove(checkout_item)
                        ListOfItem.objects.get(id=checkout_item.id).delete()
                        checkout.save()

                    remarks += item_id + ", " + quality + ", " + quantity + ";"
                    list_of_items.append(
                        [prev_sport_type, prev_name, prev_brand, quality, quantity]
                    )

                if checkin_status_count == checkout_item_list_count:
                    checkout.checkin_status = True
                    checkout.save()
                remarks += "<br>---------------------------------------<br>"
                try:
                    checkin = checkout.checkin
                    checkin.remarks += remarks
                    checkin.save()
                except:
                    checkin = Checkin(
                        checkout_item=checkout,
                        remarks=remarks,
                        created_at=D.datetime.now().date(),
                    )
                    checkin.save()

                html_message = render_to_string(
                    "mail/CheckoutMail.html",
                    {
                        "date": checkin.date_of_submit,
                        "roll_no": checkin.checkout_item.student_name.roll_no,
                        "items_detail": list_of_items,
                    },
                )
                send_mail(
                    "Checkout Detail",
                    "",
                    "kaporkhanasharma@gmail.com",
                    ["kaporkhanasharma@gmail.com"],
                    fail_silently=False,
                    html_message=html_message,
                )
                print(html_message)
                return redirect("checkin-list")
            else:
                messages.error(request, "Already checkin")
                return redirect("checkout")


# class CheckinView(View):
#     template_name ='checkin/CheckinDetail.html'
#     def get(self, request, *args, **kwargs):
#         if request.method=="GET":
#             checkout_id=kwargs["checkout_pk"]
#             return render(request,self.template_name)

# list_of_items=[]
# checkout =Checkout.objects.get(id=checkout_id)
# if not checkout.checkin_status:
#     item_list=list(checkout.item_list.values())
#     for i in item_list:
#         item            =Item.objects.get(id=i['item_id'])
#         item.available +=i['item_quantity']
#         item.save()
#         print(item.available)

#         list_of_items.append([
#             item.sport_type.name,
#             item.name,
#             item.brand,
#             item.quality,
#             i['item_quantity'],
#         ])

#     checkin =Checkin(checkout_item=checkout)
#     checkin.save()

#     html_message=render_to_string('mail/CheckoutMail.html',{
#         'date':checkin.date_of_submit,
#         'roll_no':checkin.checkout_item.student_name.roll_no,
#         'items_detail':list_of_items,
#     })
#     # print(html_message)
#     print(checkin.date_of_submit)
# send_mail(
#     'Checkout Detail',
#     '',
#     'kaporkhanasharma@gmail.com',
#     ['kaporkhanasharma@gmail.com'],
#     fail_silently=False,
#     html_message=html_message,
# )

#     checkout.checkin_status=True
#     checkout.save()
#     return redirect('checkout')
# else:
#     messages.error(request,"Already checkin")
#     return redirect('checkout')
