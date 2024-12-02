from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Item, Category, ItemPhoto, Shop


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'archived', 'updated_at', 'href')
    search_fields = ('name',)  # Enable search by category name

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password']  
    search_fields = ['username']  

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'name', 'code', 'category', 'buy_price', 'sale_price')  # Display these fields in the admin list
    search_fields = ('name', 'category__name')  # Enable search by item name and category name
    list_filter = ('category',)  # Add filter by category on the right sidebar


@admin.register(ItemPhoto)
class ItemPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'photo')
