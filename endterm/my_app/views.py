# catalog/views.py
from rest_framework import generics, status
from rest_framework.views import APIView
from .models import Category, Item, ItemPhoto, Shop
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import CategorySerializer, ItemSerializer, ItemPhotoSerializer, ShopRegisterSerializer, ShopSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListCreateAPIView, ListAPIView
from .serializers import ItemSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.shortcuts import get_object_or_404


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(shop_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(shop_id=self.request.user.id)


class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(shop_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(shop_id=self.request.user.id)


class ItemListCreateView(ListCreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        items = self.get_queryset()

        struct_response = []

        for item in items:
            item_response = {
                "item": {
                    "id": item.id,
                    "name": item.name,
                    "description": item.description,
                    "code": item.code,
                    "buy_price": item.buy_price,
                    "sale_price": item.sale_price,
                    "href": item.href,
                    "weight": item.weight,
                    "in_stock": item.in_stock,
                    "count": item.count,
                    "updated_at": item.updated_at,
                    "sale_id": item.sale_id,
                    "tags_id": item.tags_id,
                },
                "category": {
                    "id": item.category.id,
                    "name": item.category.name,
                    "archived": item.category.archived,
                    "updated_at": item.category.updated_at,
                    "href": item.category.href,
                },
                "photos": [
                    request.build_absolute_uri(photo.photo.url) for photo in item.photos.all()
                ],
            }
            struct_response.append(item_response)

        return Response(struct_response)

    def get_queryset(self):
        return Item.objects.filter(shop_id=self.request.user.id, in_stock=True)

    def perform_create(self, serializer):
        serializer.save(shop_id=self.request.user.id)


class ShopRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ShopRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Shop registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopListView(ListAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class ItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

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
                "count": instance.count,
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
            "photos": [
                request.build_absolute_uri(photo.photo.url) for photo in instance.photos.all()
            ],
        }

        return Response(struct_response)

    def get_queryset(self):
        return Item.objects.filter(shop_id=self.request.user.id)


class ItemPhotoListCreateView(generics.GenericAPIView):
    """
    API endpoint for listing and uploading photos for a specific Item.
    """
    serializer_class = ItemPhotoSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get_queryset(self, item_id):
        return ItemPhoto.objects.filter(item_id=item_id)

    def get(self, request, item_id, *args, **kwargs):
        """
        List all photos for the given Item.
        """
        photos = self.get_queryset(item_id)
        serializer = self.get_serializer(photos, many=True)
        return Response(serializer.data)

    def post(self, request, item_id, *args, **kwargs):
        """
        Upload a photo for the given Item.
        """
        try:
            # Validate that the item exists
            item = Item.objects.get(pk=item_id)
        except Item.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        # Add the item to the incoming photo data
        request.data['item'] = item_id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        product = get_object_or_404(Item, pk=pk, shop=request.user)

        decrement = request.data.get("count", 0)

        if not isinstance(decrement, int) or decrement <= 0:
            return Response({"error": "Invalid decrement value"}, status=status.HTTP_400_BAD_REQUEST)
        if product.count >= decrement:
            product.count -= decrement
            if product.count == 0:
                product.in_stock = False
            product.save()
            return Response({"message": "count decreased", "count": product.count}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Not enough count"}, status=status.HTTP_400_BAD_REQUEST)
