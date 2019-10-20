from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import View
from django.urls import reverse_lazy

from .models import Sport
from .models import Item

class HomeView(View):
    template_name = 'layout.html'
    sport   = list(Sport.objects.values())
    print("saaa")
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{'sport':self.sport})

class SportCreateView(View):
    def post(self,request):
        if request.method=="POST":
            name = request.POST.get("name")
            image = None
            if  request.FILES:
                image = request.FILES.get("image")
            print(name,image)
            sport = Sport(name=name,image=image)
            # sport.save()
            sport   = list(Sport.objects.values())
            return redirect('home')
            # return reverse_lazy('home')


class ItemCreateView(View):
    template_name ='sport/CreateItem.html'
    def get(self, request, *args, **kwargs):
        id = kwargs['sport_pk']
        return render(request,self.template_name,{'id':id})
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
            item    = Item(name=name,brand=brand,quality=quality,quantity=quantity,description=description,sport_type=sport)
            # item.save()
            return redirect('list_item',id)

class ItemListView(View):
    template_name = 'sport/Item.html'

    def get(self, request, *args, **kwargs):
        id = kwargs['item_pk']
        sport = Sport.objects.get(id=id)
        items = list(Item.objects.filter(sport_type=sport).values())
        return render(request,self.template_name,{'items':items,'id':id})


# class SportCreate(CreateView):
#     model           = Sport
#     template_name   = ''
#     fields          ='__all__'
#     success_url = reverse_lazy('#')