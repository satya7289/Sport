import datetime as D
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib import messages
from django.http import Http404
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.db.models import Q

from sport.models import Sport
from sport.models import Item
from sport.models import Student


class SportCreateView(View):
    def post(self, request):
        if request.method == "POST":
            name = request.POST.get("name")
            id = 1  # Default Id
            image = None
            if request.FILES:
                image = request.FILES.get("image")
            # print(name, image)
            if Sport.objects.filter(name=name):
                messages.error(request, "Sport Name Already Exit.")
                return redirect("home")
            sport = Sport(name=name, image=image, created_at=D.datetime.now().date())
            sport.save()
            if sport.id:
                id = sport.id
            return redirect("list_item", id)


class ItemListView(View):
    template_name = "sport/Item.html"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        id = kwargs["item_pk"]
        sport = Sport.objects.get(id=id)
        items = Item.objects.filter(sport_type=sport)
        return self.pagination(items, id, sport)

    def pagination(self, object, id, sport):
        paginator = Paginator(object, self.paginate_by)
        page = self.request.GET.get("page")
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        return render(
            self.request, self.template_name, {"items": items, "id": id, "sport": sport}
        )


class ItemCreateView(View):
    template_name = "sport/CreateItem.html"

    def get(self, request, *args, **kwargs):
        id = kwargs["sport_pk"]
        sport = Sport.objects.get(id=id)
        return render(request, self.template_name, {"id": id, "sport": sport})

    def post(self, request, *args, **kwargs):
        id = kwargs["sport_pk"]
        sport = Sport.objects.get(id=id)
        if request.method == "POST":
            name = request.POST.get("name")
            brand = request.POST.get("brand")
            quantity = request.POST.get("quantity")
            quality = request.POST.get("quality")
            description = request.POST.get("description")

            item_test = sport.item_set.filter(name=name, brand=brand, quality=quality)
            if item_test:
                message = "Item Already exit."
                return render(request, self.template_name, {"id": id, "error": message})

            # print(name,brand,quantity,quality,description,sport)
            item = Item(
                name=name,
                brand=brand,
                quality=quality,
                available=quantity,
                quantity=quantity,
                description=description,
                sport_type=sport,
                created_at=D.datetime.now().date(),
            )
            item.save()
            return redirect("list_item", id)


class EditItemView(View):
    template_name = "sport/EditItem.html"

    def get(self, request, *args, **kwargs):
        if request.method == "GET":
            sport_pk = kwargs["sport_pk"]
            id = request.GET.get("id")
            try:
                item = Item.objects.get(id=id)
                return render(
                    request, self.template_name, {"item": item, "sport_pk": sport_pk}
                )
            except Student.DoesNotExist:
                raise Http404

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            name = request.POST.get("name")
            brand = request.POST.get("brand")
            quality = request.POST.get("quality")
            description = request.POST.get("description")
            id = request.GET.get("id")
            sport_pk = kwargs["sport_pk"]
            try:
                item = Item.objects.get(id=id)
                item.name = name
                item.brand = brand
                item.quality = quality
                item.description = description
                item.save()
                return redirect("list_item", sport_pk)
            except Student.DoesNotExist:
                raise Http404


class SearchItemView(View):
    template_name = "sport/Item.html"

    def get(self, request, *args, **kwargs):
        id = kwargs["item_pk"]
        sport = Sport.objects.get(id=id)
        search_query = request.GET.get("q", "")
        search_type = request.GET.get("type", "")
        if search_type == "Name":
            data = Item.objects.filter(name__contains=search_query)
        elif search_type == "Brand":
            data = Item.objects.filter(brand__contains=search_query)
        elif search_type == "Quality":
            data = Item.objects.filter(quality__contains=search_query)
        elif search_type == "All":
            data = Item.objects.filter(
                Q(brand__contains=search_query)
                | Q(name__contains=search_query)
                | Q(quality__contains=search_query)
            )
        return render(
            request,
            self.template_name,
            {"items": data, "id": id, "sport": sport, "q": search_query},
        )
