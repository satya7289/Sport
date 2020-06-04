import datetime as D
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import Http404
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from sport.models import Sport
from sport.models import Item
from sport.models import Student
from sport.models import ListOfItem
from sport.models import Checkin
from sport.models import Checkout


class CheckoutDetailView(View):
    template_name   ='checkout/CheckoutDetail.html'
    paginate_by     =20
    def get(self, request, *args, **kwargs):
        checkouts=Checkout.objects.all()

        return self.pagination(checkouts)

    def pagination(self, object):
        paginator = Paginator(object, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            checkouts = paginator.page(page)
        except PageNotAnInteger:
            checkouts = paginator.page(1)
        except EmptyPage:
            checkouts = paginator.page(paginator.num_pages)
        return render(self.request, self.template_name, {'checkouts':checkouts})


class CheckoutView(View):
    template_name   ='checkout/Checkout.html'
    def get(self, request, *args, **kwargs):
        sports   =list(Sport.objects.values())
        items    =list(Item.objects.values())
        students =list(Student.objects.values())
        return render(request,self.template_name,{
            'sports':sports,
            'items':items, 
            'students':students,
            })

    def post(self, request, *args, **kwargs):
        if request.method=="POST":
            roll_no    =request.POST.get("student-roll-no")
            list_of_item_input = []
            number_of_items =[]
            list_of_items =[]

            student =Student.objects.filter(roll_no=roll_no).first()
            checkout=Checkout(student_name=student)
            checkout.save()

            for key in request.POST:
                list_of_item_input.append(key)
            del list_of_item_input[0:2]
            
            for i in range(int(len(list_of_item_input)/5)):
                number_of_items.append(list_of_item_input[i*5:i*5+5])
            for i in number_of_items:
                sport_name=request.POST.get(i[0])
                item_name =request.POST.get(i[1])
                brand   =request.POST.get(i[2])
                quality =request.POST.get(i[3])
                quantity=request.POST.get(i[4])

                sport =Sport.objects.filter(name=sport_name).first()
                item  =Item.objects.filter(name=item_name,brand=brand,quality=quality,sport_type=sport).first()
                item.available -=int(quantity)
                
                if item.available < 0:
                    messages.error(request,"Dublicate Data is entered ")
                    return redirect('checkout')

                item.save()
                # print(item.available,"xdcfvgbhnjmk,")

                new_item =ListOfItem(item=item,item_quantity=quantity)
                new_item.save()
                checkout.item_list.add(new_item)

                list_of_items.append([
                    sport_name,
                    item_name,
                    brand,
                    quality,
                    quantity,
                ])

                # print(item.available,new_item)

            print(roll_no,list_of_items)
            html_message=render_to_string('mail/CheckoutMail.html',{
                'date':checkout.date_of_issue,
                'roll_no':roll_no,
                'items_detail':list_of_items,
            })
            
            # send_mail(
            #     'Checkout Detail',
            #     '',
            #     'kaporkhanasharma@gmail.com',
            #     ['kaporkhanasharma@gmail.com'],
            #     fail_silently=False,
            #     html_message=html_message,
            # )
            
            return redirect('checkout')
