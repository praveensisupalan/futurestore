from django.urls import path
from rest_framework.routers import DefaultRouter
from storeapi import views

router = DefaultRouter()
router.register('v1/registration', views.UserView, basename="register")
router.register("v1/category", views.CategoryView, basename="category")
router.register("v1/products", views.ProductsView, basename="products")
router.register('v1/cart', views.CartView, basename="cart")
urlpatterns = [] + router.urls
