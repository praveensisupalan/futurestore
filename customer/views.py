from django.shortcuts import render, redirect
from django.views.generic import View, CreateView, TemplateView, FormView, DetailView, ListView
from customer import forms
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from owner import models
from django.contrib import messages
from customer.decorators import signin_required
from django.utils.decorators import method_decorator


# Create your views here.

class RegistrationView(CreateView):
    form_class = forms.RegistrationForm
    template_name = "registration.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        messages.success(self.request, "your account has been created")
        return super().form_valid(form)


class LoginView(FormView):
    template_name = "login.html"
    form_class = forms.LoginForm

    def post(self, request, *args, **kwargs):
        form = forms.LoginForm(request.POST, files=request.FILES)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if request.user.is_superuser:
                    return redirect("dashboard")
                else:
                    return redirect("home")
            else:
                messages.error(request, "login failed!"
                                        " invalid username or password")
                return render(request, "login.html", {"form": form})


@method_decorator(signin_required, name="dispatch")
class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = models.Products.objects.all()
        return context


@method_decorator(signin_required, name="dispatch")
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")


@method_decorator(signin_required, name="dispatch")
class ProductDetailView(DetailView):
    template_name = "product_detail.html"
    model = models.Products
    context_object_name = "product"
    pk_url_kwarg = "id"


@method_decorator(signin_required, name="dispatch")
class AddToCartView(FormView):
    template_name = "add_to_cart.html"
    form_class = forms.CartForm

    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        product = models.Products.objects.get(id=id)

        return render(request, self.template_name, {"form": forms.CartForm(), "product": product})

    def post(self, request, *args, **kwargs):
        id = kwargs.get("id")
        product = models.Products.objects.get(id=id)
        qty = request.POST.get("qty")
        user = request.user
        models.Cart.objects.create(product=product, user=user, qty=qty)
        messages.success(request, "item added to cart")
        return redirect("home")


@method_decorator(signin_required, name="dispatch")
class MyCatrView(ListView):
    model = models.Cart
    template_name = "cart_list.html"
    context_object_name = "carts"

    def get_queryset(self):
        return models.Cart.objects.filter(user=self.request.user).exclude(status="canceled").order_by("-created_date")


@signin_required
def remove_from_cart(request, *args, **kwargs):
    cart_id = kwargs.get("id")
    cart_prod = models.Cart.objects.get(id=cart_id)
    cart_prod.status = "canceled"
    cart_prod.save()
    messages.success(request, "REMOVED")
    return redirect("mycart")


@method_decorator(signin_required, name="dispatch")
class PlaceOrderView(FormView):
    template_name = "place_order.html"
    form_class = forms.OrderFrom

    def post(self, request, *args, **kwargs):
        cart_id = kwargs.get("cid")
        product_id = kwargs.get("pid")
        cart = models.Cart.objects.get(id=cart_id)
        product = models.Products.objects.get(id=product_id)
        user = request.user
        delivery_address = request.POST.get("delivery_address")
        models.Orders.objects.create(product=product, user=user, delivery_address=delivery_address)
        cart.status = "order-placed"
        cart.save()
        messages.success(request, "order placed")
        return redirect("home")
