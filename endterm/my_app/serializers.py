from rest_framework import serializers
from .models import Category, Item, ItemPhoto


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'archived', 'updated_at', 'href']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'code', 'buy_price', 'sale_price', 'category', 'href', 'weight',
                  'in_stock', 'updated_at', 'sale_id', 'tags_id']


class ItemPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPhoto
        fields = ['id', 'item', 'photo']
        read_only_fields = ['id']
