from rest_framework import serializers
from django.contrib.auth.models import User
from owner.models import Categorys, Products, Cart, Orders


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Categorys
        fields = ["id", "category_name", "is_active"]

        
class ProductsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Products
        fields = ["id", "product_name", "category", "image", "price", "description"]


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CartSerializer(serializers.ModelSerializer):
    product = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    created_date = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Cart
        fields = ["product", "user", "created_date", "status", "qty"]


class OrdersSerializer(serializers.ModelSerializer):
    product = serializers.CharField(read_only=True)
    user = serializers.CharField(read_only=True)
    date = serializers.DateField(read_only=True)
    expected_delivery_date = serializers.DateField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        models = Orders
        fields = ["product", "user", "date", "delivery_address", "expected_delivery_date", "status"]
