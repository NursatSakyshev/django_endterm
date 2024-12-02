# catalog/urls.py
from django.urls import path
from .views import CategoryListCreateView, CategoryRetrieveUpdateDestroyView, ItemListCreateView, \
    ItemRetrieveUpdateDestroyView, ItemPhotoListCreateView, ShopRegisterView, ShopListView
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category-detail'),
    path('register/', ShopRegisterView.as_view(), name='shop_register'),
    path('items/', ItemListCreateView.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemRetrieveUpdateDestroyView.as_view(), name='item-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('items/<int:item_id>/photos/', ItemPhotoListCreateView.as_view(), name='item_photos'),

    path('shops/', ShopListView.as_view(), name='shop-list'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)