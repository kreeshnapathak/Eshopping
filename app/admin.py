from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse


from .models import (
    Customer,
    Product,
    Cart,
    OrderPlaced
)



@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'name','mobile', 'locality', 'city', 'zipcode', 'state']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price','product_det', 'discounted_price', 
    'description', 'brand', 'category', 'product_image']

    def product_det(self, obj):
        link = reverse('admin:app_product_change',args=[obj.pk])
        return format_html('<a href = "{}">{}</a>' , link, obj.title)
    

    

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'product_det','customer_det','quantity', 'ordered_date', 'status']

    def product_det(self, obj):
        link = reverse('admin:app_product_change',args=[obj.product.pk])
        return format_html('<a href = "{}">{}</a>' , link, obj.product.title)
    
    def customer_det(self, obj):
        link = reverse('admin:app_customer_change',args=[obj.customer.pk])
        return format_html('<a href = "{}">{}</a>' , link, obj.customer.name)
    

