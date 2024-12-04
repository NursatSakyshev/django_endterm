from django.conf import settings
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from my_app.models import Category, Item, Shop
import django
import os


class APITests(APITestCase):
    def setUp(self):
        """
        Set up test data and authentication.
        """
        # Create a test user and obtain JWT token
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

        # Authenticate the client
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        # Test data
        self.category = Category.objects.create(name="Test Category")
        self.shop = Shop.objects.create(name="Test Shop", owner=self.user)
        self.item = Item.objects.create(name="Test Item", shop=self.shop, price=10)

    def test_category_list_create(self):
        """
        Test GET and POST for /categories/
        """
        # Test GET
        response = self.client.get("/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test POST
        response = self.client.post("/categories/", {"name": "New Category"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_category_retrieve_update_destroy(self):
        """
        Test GET, PUT, PATCH, DELETE for /categories/<int:pk>/
        """
        # Test GET
        response = self.client.get(f"/categories/{self.category.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test PATCH
        response = self.client.patch(f"/categories/{self.category.id}/", {"name": "Updated Category"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test DELETE
        response = self.client.delete(f"/categories/{self.category.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_shop_register(self):
        """
        Test POST for /register/
        """
        response = self.client.post("/register/", {"name": "New Shop"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_item_list_create(self):
        """
        Test GET and POST for /items/
        """
        # Test GET
        response = self.client.get("/items/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test POST
        response = self.client.post("/items/", {"name": "New Item", "price": 20, "shop": self.shop.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_item_retrieve_update_destroy(self):
        """
        Test GET, PUT, PATCH, DELETE for /items/<int:pk>/
        """
        # Test GET
        response = self.client.get(f"/items/{self.item.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test PATCH
        response = self.client.patch(f"/items/{self.item.id}/", {"price": 15})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test DELETE
        response = self.client.delete(f"/items/{self.item.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_item_transaction(self):
        """
        Test POST for /items/<int:pk>/transaction/
        """
        response = self.client.post(f"/items/{self.item.id}/transaction/", {"decrement": 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_item_photos(self):
        """
        Test GET and POST for /items/<int:item_id>/photos/
        """
        # Test GET
        response = self.client.get(f"/items/{self.item.id}/photos/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test POST
        response = self.client.post(
            f"/items/{self.item.id}/photos/",
            {"photo": "test_photo.jpg"}  # Assuming you handle file uploads
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_shop_list(self):
        """
        Test GET for /shops/
        """
        response = self.client.get("/shops/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_obtain(self):
        """
        Test POST for /token/
        """
        response = self.client.post("/token/", {"username": "testuser", "password": "password123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_refresh(self):
        """
        Test POST for /token/refresh/
        """
        response = self.client.post("/token/refresh/", {"refresh": str(self.refresh)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
