from django.contrib import admin
from .models import Order, OrderTransaction

admin.site.register(Order)
admin.site.register(OrderTransaction)
