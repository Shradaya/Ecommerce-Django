from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([Category, Product, Cart, CartProduct, message])

@admin.register(Order)
class OrderTable(admin.ModelAdmin):
    list_display=("cart", "ordered_by", "shipping_address","order_status",
        "mobile", "payment_method","payment_completed","delivery_completed")
