# Generated by Django 5.1.3 on 2024-11-14 16:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("archived", models.BooleanField(default=False)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("href", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("code", models.CharField(max_length=255)),
                ("buy_price", models.FloatField()),
                ("sale_price", models.FloatField()),
                ("href", models.URLField()),
                ("weight", models.FloatField()),
                ("in_stock", models.BooleanField(default=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("sale_id", models.IntegerField()),
                ("tags_id", models.IntegerField()),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="my_app.category",
                    ),
                ),
            ],
        ),
    ]