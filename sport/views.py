from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Sport
from .models import Item
from .models import Student

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
            sport   =Sport.objects.get(name=team)
            if Student.objects.filter(roll_no=roll_no):
                messages.error(request,"Roll No Already Exits.")
                return render(request,self.template_name)
            student   =Student(first_name=first_name,last_name=last_name,roll_no=roll_no,email=email)
            student.save()
            sport.student_set.add(student)
            print(first_name,last_name,roll_no,email,team,sport)
            return redirect('students')


class CheckoutView(View):
    template_name   ='checkout/Checkout.html'
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)