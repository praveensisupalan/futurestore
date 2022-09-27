from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.


class Categorys(models.Model):
    category_name = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.category_name


class Products(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Categorys, on_delete=models.CASCADE)
    image = models.ImageField()
    price = models.PositiveIntegerField()
    discription = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.product_name


class Cart(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    options = (
        ("incart", "incart"),
        ("Order-placed", "Ordered-placed"),
        ("cancled", "cancled")
    )
    status = models.CharField(max_length=12, choices=options, default="incart")
    qty = models.PositiveIntegerField()


class Review(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    rating = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])


class Order(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True, null=True)
    options = (
        ("order-placed", "order-placed"),
        ("shiped", "shiped"),
        ("in-transit", "in-transit"),
        ("delivered", "delivered")
    )
    status = models.CharField(max_length=12, choices=options, default="order-placed")
