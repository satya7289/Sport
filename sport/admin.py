from django.contrib import admin
from .models import Sport
from .models import Item
from .models import Student

admin.site.register(Sport)
admin.site.register(Item)
admin.site.register(Student)