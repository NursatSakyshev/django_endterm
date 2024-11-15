# catalog/views.py
from rest_framework import generics
from .models import Category, Item
from .serializers import CategorySerializer, ItemSerializer
from rest_framework.response import Response


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get(self, request, *args, **kwargs):
        # Retrieve the item instance based on the URL parameter (e.g., `pk`)
        instance = self.get_object()

        # Construct a structured response
        struct_response = {
            "item": {
                "id": instance.id,
                "name": instance.name,
                "description": instance.description,
                "code": instance.code,
                "buy_price": instance.buy_price,
                "sale_price": instance.sale_price,
                "href": instance.href,
                "weight": instance.weight,
                "in_stock": instance.in_stock,
                "updated_at": instance.updated_at,
                "sale_id": instance.sale_id,
                "tags_id": instance.tags_id,
            },
            "category": {
                "id": instance.category.id,
                "name": instance.category.name,
                "archived": instance.category.archived,
                "updated_at": instance.category.updated_at,
                "href": instance.category.href,
            },
        }

        return Response(struct_response)
