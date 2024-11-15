# catalog/urls.py
from django.urls import path
from .views import CategoryListCreateView, CategoryRetrieveUpdateDestroyView, ItemListCreateView, \
    ItemRetrieveUpdateDestroyView, ItemPhotoListCreateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),

    path('items/', ItemListCreateView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemRetrieveUpdateDestroyView.as_view(), name='item-detail'),

    path('items/<int:item_id>/photos/', ItemPhotoListCreateView.as_view(), name='item_photos'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)