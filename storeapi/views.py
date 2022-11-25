from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from storeapi.serializer import UserSerializer, CategorySerializer, ProductsSerializer,CartSerializer
from django.contrib.auth.models import User
from owner.models import Categorys, Products, Cart


# Create your views here.

class UserView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CategoryView(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Categorys.objects.all()


class ProductsView(ModelViewSet):
    serializer_class = ProductsSerializer
    queryset = Products.objects.all()


class CartView(ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
