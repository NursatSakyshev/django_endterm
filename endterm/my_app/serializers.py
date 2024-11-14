from rest_framework import serializers
from .models import Category, Item

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'archived', 'updated_at', 'href']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'code', 'buy_price', 'sale_price', 'category', 'href', 'weight', 'in_stock', 'updated_at', 'sale_id', 'tags_id']
