from django.urls import path
from django.views.generic import TemplateView

from sport.view.view import HomeView

from sport.view.sport_view import SportCreateView
from sport.view.sport_view import ItemCreateView
from sport.view.sport_view import ItemListView
from sport.view.sport_view import EditItemView
from sport.view.sport_view import SearchItemView

from sport.view.student_view import StudentListView
from sport.view.student_view import StudentCreateView
from sport.view.student_view import EditStudentView
from sport.view.student_view import SearchStudentView

from sport.view.checkout_view import CheckoutDetailView
from sport.view.checkout_view import CheckoutView

from sport.view.checkin_view import CheckinListView
from sport.view.checkin_view import CheckinDetailView
from sport.view.checkin_view import CheckinView


from sport.view import api_view

urlpatterns = [
    # path('',TemplateView.as_view(template_name='home.html'))
    path("", HomeView.as_view(), name="home"),
    path("item/", TemplateView.as_view(template_name="sport/CreateItem.html")),
    path("additem/<int:sport_pk>/", ItemCreateView.as_view(), name="add_item"),
    path("item/<int:item_pk>/", ItemListView.as_view(), name="list_item"),
    path("addsport/", SportCreateView.as_view(), name="add_sport"),
    path("item/<int:sport_pk>/edit-item", EditItemView.as_view(), name="edit-item"),
    path("item/<int:item_pk>/search", SearchItemView.as_view(), name="search_sport"),
    path("students/", StudentListView.as_view(), name="students"),
    path("addstudent/", StudentCreateView.as_view(), name="add_student"),
    path("editstudent", EditStudentView.as_view(), name="edit-student"),
    path("students/search", SearchStudentView.as_view(), name="search_student"),
    path("checkout/detail", CheckoutDetailView.as_view(), name="checkout-detail"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("checkin/", CheckinListView.as_view(), name="checkin-list"),
    path(
        "checkin/<int:checkout_pk>/", CheckinDetailView.as_view(), name="checkin-detail"
    ),
    path("post-checkin", CheckinView.as_view(), name="post-checkin"),
    path("ajax/allsport/", api_view.GetAllSport, name="all_sport"),
    path("ajax/sport", api_view.GetSport, name="sport"),
    path("ajax/search", api_view.Search, name="api_search"),
    path("ajax/checkout", api_view.CheckoutDetail, name="ajax-checkout-detail"),
]
