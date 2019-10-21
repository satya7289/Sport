from django.urls import path
from django.views.generic import TemplateView

from .views import SportCreateView
from .views import ItemCreateView
from .views import HomeView
from .views import ItemListView
from .views import StudentListView
from .views import CheckoutView

from . import api_view

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('item/',TemplateView.as_view(template_name="sport/CreateItem.html")),
    path('add_item/<int:sport_pk>/',ItemCreateView.as_view(),name='add_item'),
    path('item/<int:item_pk>/',ItemListView.as_view(),name='list_item'),
    path('addsport/',SportCreateView.as_view(),name='add_sport'),

    path('students/',StudentListView.as_view(),name='students'),
    path('checkout/',CheckoutView.as_view(),name='checkout'),


    path('api/allsport/',api_view.GetAllSport,name='all_sport'),
    path('api/sport',api_view.GetSport,name='sport'),

]
