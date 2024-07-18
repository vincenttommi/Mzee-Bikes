from django.contrib import admin
from  .models import Bicycle,Order,CartItem


admin.site.register(Bicycle)
admin.site.register(Order)
admin.site.register(CartItem)