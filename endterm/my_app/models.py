from django.db import models

# Create your models here.
from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    archived = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    href = models.URLField(max_length=200)

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
    sale_id = models.IntegerField()
    tags_id = models.IntegerField()

    def __str__(self):
        return self.name


class ItemPhoto(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='item_photos/')

    def __str__(self):
        return f"Photo for {self.item.name}"