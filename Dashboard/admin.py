from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Food_Category)
admin.site.register(Food_Item)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)