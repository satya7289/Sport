from django.shortcuts import render
from django.views.generic import View


class HomeView(View):
    template_name = "layout.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
