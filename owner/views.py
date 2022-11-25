from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from owner.models import Orders, Categorys, Products
from owner.forms import OrderUpdateForm
from django.core.mail import send_mail
from customer.decorators import signin_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy


# Create your views here.
@method_decorator(signin_required, name="dispatch")
class AdminDashboardView(TemplateView):
    template_name = "owner/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cnt = Orders.objects.filter(status="order-placed").count
        context["count"] = cnt
        return context


@method_decorator(signin_required, name="dispatch")
class OrdersListView(ListView):
    model = Orders
    template_name = "owner/orders_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Orders.objects.filter(status="order-placed")


@method_decorator(signin_required, name="dispatch")
class OrderDetailView(DetailView):
    model = Orders
    template_name = "owner/order_detail.html"
    pk_url_kwarg = "id"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = OrderUpdateForm
        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        form = OrderUpdateForm(request.POST)
        if form.is_valid():
            order.status = form.cleaned_data.get("status")
            order.expected_delivery_date = form.cleaned_data.get("expected_delivery_date")
            order.save()
            dt = form.cleaned_data.get("expected_delivery_date")
            send_mail(
                "order conformation",
                f"Hai {request.user} your order has been conformed and expected to delivered on{dt}",
                "praveensisuplan34@gmail.com",
                ["praveenvandnam16@gmail.com"]
            )
        return redirect("dashboard")


