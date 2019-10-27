from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Sport
from .models import Item
from .models import Student
from .models import ListOfItem
from .models import Checkin
from .models import Checkout

class HomeView(View):
    template_name = 'layout.html'
    sport   = list(Sport.objects.values())
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{'sport':self.sport})

class SportCreateView(View):
    def post(self,request):
        if request.method=="POST":
            name = request.POST.get("name")
            id = 1      # Default Id 
            image = None
            if  request.FILES:
                image = request.FILES.get("image")
            print(name,image)
            if Sport.objects.filter(name=name):
                messages.error(request,"Sport Name Already Exit.")
                return redirect('home')
            sport = Sport(name=name,image=image)
            sport.save()
            if sport.id:
                id = sport.id
            return redirect('list_item',id)


class ItemCreateView(View):
    template_name ='sport/CreateItem.html'
    def get(self, request, *args, **kwargs):
        id = kwargs['sport_pk']
        sport = Sport.objects.get(id=id)
        return render(request,self.template_name,{'id':id,'sport':sport})
    def post(self, request, *args, **kwargs):
        id     = kwargs['sport_pk']
        sport  = Sport.objects.get(id=id)
        if request.method=="POST":
            name    =request.POST.get("name")
            brand   =request.POST.get("brand")
            quantity=request.POST.get("quantity")
            quality =request.POST.get("quality")
            description=request.POST.get("description")
            
            item_test =  sport.item_set.filter(name=name)
            if item_test:
                message = "Name of the Item Already exit."
                return render(request,self.template_name,{'id':id,'error':message})

            print(name,brand,quantity,quality,description,sport)
            item    = Item(name=name,brand=brand,quality=quality,available=quantity,quantity=quantity,description=description,sport_type=sport)
            item.save()
            return redirect('list_item',id)

class ItemListView(View):
    template_name = 'sport/Item.html'

    def get(self, request, *args, **kwargs):
        id = kwargs['item_pk']
        sport = Sport.objects.get(id=id)
        items = list(Item.objects.filter(sport_type=sport).values())
        return render(request,self.template_name,{'items':items,'id':id,'sport':sport})

class StudentListView(View):
    template_name   ='student/Students.html'
    def get(self, request, *args, **kwargs):
        students = list(Student.objects.values())
        for student in students:
            sport = Student.objects.get(id=student['id']).team.first().name
            student['sport']=sport
        return render(request,self.template_name,{'students':students})
        

class StudentCreateView(View):
    template_name ='student/CreateStudent.html'
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)
    def post(self, request, *args, **kwargs):
        if request.method=="POST":
            first_name  =request.POST.get("first-name")
            last_name   =request.POST.get("last-name")
            roll_no     =request.POST.get("roll-no")
            email       =request.POST.get("email")
            team        =request.POST.get("sport-name")

            # print(first_name,last_name,roll_no,email,team)
            # Get sport by team name
            if team:
                sport   =Sport.objects.filter(name=team).first()
                if Student.objects.filter(roll_no=roll_no):
                    messages.error(request,"Roll No Already Exits.")
                    return render(request,self.template_name)
                student   =Student(first_name=first_name,last_name=last_name,roll_no=roll_no,email=email)
                student.save()
                sport.student_set.add(student)
                print(first_name,last_name,roll_no,email,team,sport)
                return redirect('students')
            messages.error(request,"Enter Sport Name")
            return render(request,self.template_name)


class CheckoutView(View):
    template_name   ='checkout/Checkout.html'
    def get(self, request, *args, **kwargs):
        sports   =list(Sport.objects.values())
        items    =list(Item.objects.values())
        students =list(Student.objects.values())
        checkouts=list(Checkout.objects.values())
        return render(request,self.template_name,{
            'sports':sports,
            'items':items, 
            'students':students,
            'checkouts':checkouts,
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
            html_message=render_to_string('mail.html',{
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

class CheckinView(View):
    def get(self, request, *args, **kwargs):
        if request.method=="GET":
            checkout_id=kwargs["checkout_pk"]

            checkout =Checkout.objects.get(id=checkout_id)
            if not checkout.checkin_status:
                checkout.checkin_status=True
                checkout.save()
                item_list=list(checkout.item_list.values())
                for i in item_list:
                    item            =Item.objects.get(id=i['item_id'])
                    item.available +=i['item_quantity']
                    item.save()
                    print(item.available)
                
                checkin =Checkin(checkout_item=checkout)
                checkin.save()
                return redirect('checkout')
            else:
                messages.error(request,"Already checkin")
                return redirect('checkout')
    
    def post(self, request, *args, **kwargs):
        pass

