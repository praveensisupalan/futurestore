from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.


class Categorys(models.Model):
    category_name = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name


class Products(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Categorys, on_delete=models.CASCADE)
    image = models.ImageField()
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    options = (
        ("in-cart", "in-cart"),
        ("order-placed", "ordered-placed"),
        ("canceled", "canceled")
    )
    status = models.CharField(max_length=12, choices=options, default="in-cart")
    qty = models.PositiveIntegerField()


class Reviews(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])


class Orders(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, null=True)
    delivery_address = models.CharField(max_length=200, null=True)
    expected_delivery_date = models.DateTimeField(null=True)
    options = (
        ("order-placed", "order-placed"),
        ("dispatched", "dispatched"),
        ("in-transit", "in-transit"),
        ("delivered", "delivered")
    )
    status = models.CharField(max_length=12, choices=options, default="order-placed")
