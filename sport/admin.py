from django.contrib import admin
from .models import Sport
from .models import Item
from .models import Student
from .models import Checkin
from .models import Checkout
from .models import ListOfItem

admin.site.register(Sport)
admin.site.register(Item)
admin.site.register(Student)
admin.site.register(Checkout)
admin.site.register(Checkin)
admin.site.register(ListOfItem)
