from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import BaseUserManager


class ShopManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, name):
        return self.get(username=name)


class Shop(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)

    objects = ShopManager()

    def __str__(self):
        return self.username


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    archived = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    href = models.URLField(max_length=200)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    code = models.CharField(max_length=255)
    buy_price = models.FloatField()
    sale_price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    href = models.URLField(max_length=200)
    weight = models.FloatField()
    in_stock = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    sale_id = models.IntegerField()
    tags_id = models.IntegerField()

    def __str__(self):
        return self.name


class ItemPhoto(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='item_photos/')

    def __str__(self):
        return f"Photo for {self.item.name}"


class PreOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="preorders")
    arrival_date = models.DateField()
    quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"PreOrder for {self.item.name} by {self.shop.username}"

    def complete_order(self):
        print("complete order getted")
        """Mark the preorder as completed and update the product's quantity."""
        if self.status == 'pending':
            self.item.count += self.quantity
            self.item.save()
            self.status = 'completed'
            self.save()
