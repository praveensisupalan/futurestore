from django.urls import path
from owner import views

urlpatterns = [
  path("admin-dashboard",views.AdminDashboardView.as_view(),name="dashboard"),
  path("orders/latest",views.OrdersListView.as_view(),name="orders_list"),
  path("orders/latest/detail/<int:id>",views.OrderDetailView.as_view(),name="order_detail"),
]
