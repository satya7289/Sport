from django.urls import path
from django.views.generic import TemplateView

from .views import SportCreateView
from .views import ItemCreateView
from .views import HomeView
from .views import ItemListView
from .views import StudentListView
from .views import CheckoutView
from .views import CheckinView
from .views import StudentCreateView
from .views import CheckoutDetailView
from .views import SearchItemView
from .views import SearchStudentView

from . import api_view

urlpatterns = [
    path('',TemplateView.as_view(template_name='home.html'))

    path('',HomeView.as_view(),name='home'),
    path('item/',TemplateView.as_view(template_name="sport/CreateItem.html")),
    path('additem/<int:sport_pk>/',ItemCreateView.as_view(),name='add_item'),
    path('item/<int:item_pk>/',ItemListView.as_view(),name='list_item'),
    path('addsport/',SportCreateView.as_view(),name='add_sport'),
    path('item/<int:item_pk>/search',SearchItemView.as_view(),name='search_sport'),

    path('students/',StudentListView.as_view(),name='students'),
    path('addstudent/',StudentCreateView.as_view(),name='add_student'),
    path('students/search',SearchStudentView.as_view(),name='search_student'),

    path('checkout/detail',CheckoutDetailView.as_view(),name='checkout-detail'),
    path('checkout/',CheckoutView.as_view(),name='checkout'),
    path('checkin/<int:checkout_pk>/',CheckinView.as_view(),name='checkin'),


    path('ajax/allsport/',api_view.GetAllSport,name='all_sport'),
    path('ajax/sport',api_view.GetSport,name='sport'),
    path('ajax/search',api_view.Search,name='api_search'),
    path('ajax/checkout',api_view.CheckoutDetail,name='ajax-checkout-detail')

]
