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


class HomeView(View):
    template_name = 'layout.html'
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)
