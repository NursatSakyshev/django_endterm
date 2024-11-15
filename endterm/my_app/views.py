# catalog/views.py
from rest_framework import generics, status
from .models import Category, Item, ItemPhoto
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import CategorySerializer, ItemSerializer, ItemPhotoSerializer
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
            "photos": [
                request.build_absolute_uri(photo.photo.url) for photo in instance.photos.all()
            ],
        }

        return Response(struct_response)


class ItemPhotoListCreateView(generics.GenericAPIView):
    """
    API endpoint for listing and uploading photos for a specific Item.
    """
    serializer_class = ItemPhotoSerializer
    parser_classes = [MultiPartParser, FormParser]

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