from django.contrib import admin
from .models import Category, Product, Cart, CartItem

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'cart', 'quantity', 'is_active')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)