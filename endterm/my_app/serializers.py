from rest_framework import serializers
from .models import Category, Item, ItemPhoto, Shop
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'archived', 'updated_at', 'href']


class ShopTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        shop = self.user
        data['shop_name'] = shop.name
        return data


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'code', 'buy_price', 'sale_price', 'category', 'href', 'weight',
                  'in_stock', 'updated_at', 'sale_id', 'tags_id']

    def create(self, validated_data):
        user = self.context['request'].user

        validated_data['shop'] = user.id

        return super().create(validated_data)


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class ItemPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPhoto
        fields = ['id', 'item', 'photo']
        read_only_fields = ['id']


class ShopRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Shop
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        shop = Shop(**validated_data)
        shop.is_superuser = True
        shop.is_staff = True
        shop.set_password(password)
        shop.save()
        return shop
