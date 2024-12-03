from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Item, Category, ItemPhoto, Shop, PreOrder


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'archived', 'updated_at', 'href')
    search_fields = ('name',)  # Enable search by category name

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(shop_id=request.user.id)


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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(shop_id=request.user.id)


@admin.register(ItemPhoto)
class ItemPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'photo')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(item__shop_id=request.user.id)


@admin.register(PreOrder)
class PreOrderAdmin(admin.ModelAdmin):
    list_display = ['item', 'shop', 'arrival_date', 'status', 'quantity']
    readonly_fields = ['status']  # Запретить изменение статуса вручную

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.shop = request.user  # Привязать к текущему администратору
        super().save_model(request, obj, form, change)
