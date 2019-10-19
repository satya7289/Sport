from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('',TemplateView.as_view(template_name="layout.html")),
    path('item/',TemplateView.as_view(template_name="sport/Item.html")),

]
