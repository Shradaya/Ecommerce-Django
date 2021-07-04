from django.views.generic import TemplateView, View, CreateView, FormView, DetailView
from django.core.paginator import Paginator
from .models import *
from ecom.models import Order
from django.contrib import messages
from django.shortcuts import redirect
from .forms import *
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
#from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


class CustomerRegistrationView(CreateView):
    template_name = "customerregistration.html"
    form_class = CustomerRegistrationForm

    def post(self, form):
        form = CustomerRegistrationForm(self.request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            email = form.cleaned_data.get("email")
            user_obj = User.objects.create_user(username, email, password)
            form.instance.user = user_obj
            post = form.save(commit=False)
            post.save()
            login(self.request, user_obj)
            return redirect('Homepage')
        else:
            form = CustomerRegistrationForm()
            return render(self.request, "customerregistration.html", {'form': form, 'error':'username already in use'})

        return render(self.request, "customerregistration.html", {'form': form})


class CustomerLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("Homepage")


class CustomerLoginView(FormView):
    template_name = "customerlogin.html"
    form_class = CustomerLoginForm

    # form_valid method is a type of post method and is available in createview formview and updateview
    def form_valid(self, form):
        uname = form.cleaned_data.get("username")
        pword = form.cleaned_data["password"]
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
            return redirect('Homepage')
        else:
            return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid Username or Password."})
        return super().form_valid(form)

    def get_success_url(self):
        return redirect("Homepage")


class CustomerProfileView(TemplateView):
    template_name = "customerprofile.html"

    def get_context_data(self):
        if self.request.user.is_authenticated and Customer.objects.filter(user=self.request.user).exists():
            pass
        else:
            return redirect("/login/?next=/profile/")
        context = super().get_context_data()
        customer = self.request.user.customer
        context['customer'] = customer
        orders = Order.objects.filter(cart__customer=customer).order_by("-id")
        context["orders"] = orders
        return context


class CustomerOrderDetailView(DetailView):
    template_name = "customerorderdetail.html"
    model = Order

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated and Customer.objects.filter(user=self.request.user).exists():
            context = super().get_context_data()
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            context["ord_obj"]=order
            if self.request.user.customer != order.cart.customer:
                return redirect("customerprofile")
            else:
                return context
        else:
            return redirect("/login/?next=/profile/")

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'NasoHandmade',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password/password_reset.html", context={"form":password_reset_form})
