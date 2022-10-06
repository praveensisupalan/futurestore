from django.urls import path
from customer import views

urlpatterns = [
    path("", views.LoginView.as_view(), name="login"),
    path("register", views.RegistrationView.as_view(), name="registration"),
    path("home", views.HomeView.as_view(), name="home"),
    path("products/<int:id>", views.ProductDetailView.as_view(), name="product_detail"),
    path("products/<int:id>/cart/add", views.AddToCartView.as_view(), name="add_to_cart"),
    path("cart/all",views.MyCatrView.as_view(),name="mycart"),
    path("cart/place_order/<int:cid>/<int:pid>",views.PlaceOrderView.as_view(),name="place_order"),
]
