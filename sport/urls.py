from django.urls import path
from django.views.generic import TemplateView

from .views import SportCreateView
from .views import ItemCreateView
from .views import HomeView
from .views import ItemListView

urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('item/',TemplateView.as_view(template_name="sport/CreateItem.html")),
    path('add_item/<int:sport_pk>/',ItemCreateView.as_view(),name='add_item'),
    path('item/<int:item_pk>/',ItemListView.as_view(),name='list_item'),
    path('addsport/',SportCreateView.as_view(),name='add_sport'),

]
