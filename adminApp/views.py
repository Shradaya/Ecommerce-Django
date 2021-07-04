from django.shortcuts import render
from .models import AdminUser
from ecom.models import Order, Product, message
from django.shortcuts import redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView, View, CreateView, FormView, DetailView

class adminLogin(TemplateView):
    template_name = "adminpages/adminlogin.html"
    form_class = AdminLoginForm
    success_url = 'adminHome'
    def get(self, *args):
        form=AdminLoginForm()
        return render(self.request, self.template_name,{'form':form})
    def post(self, form):
        form = AdminLoginForm(self.request.POST or None)
        if form.is_valid():
            uname = form.cleaned_data.get("username")
            pword = form.cleaned_data.get("password")
            usr = authenticate(username=uname, password=pword)
            if usr is not None and AdminUser.objects.filter(user=usr).exists():
                login(self.request, usr)
                return redirect('adminHome')
            else:
                return render(self.request, self.template_name, {"form": self.form_class, "error": "Invalid Username or Password."})


class adminHomePage(TemplateView):
    template_name = "AdminPages/adminHome.html"

    def get(self, *args):
        if self.request.user is not None and AdminUser.objects.filter(user=self.request.user).exists():
            Orders = Order.objects.exclude(order_status="Order Completed").order_by('-created_at')
            return render(self.request, self.template_name, {"Orders":Orders, "title":"PENDING ORDERS"})
        else:
            return render(self.request, "home.html")

class messages(View):
    def get(self, *args):
        if self.request.user.is_authenticated and AdminUser.objects.filter(user=self.request.user).exists():
            msg = message.objects.all().order_by('-Date')
            return render(self.request, "AdminPages/messages.html", {'msg':msg})
        else:
            return redirect('/')

class ManageOrder(TemplateView):
    template_name = "AdminPages/adminHome.html"
    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs['o_id']
        action = request.GET.get("action")
        order_obj = Order.objects.get(id=order_id)

        if action == "OP":
            order_obj.order_status = "Order Processing"
            order_obj.save()
        elif action == "OTW":
            order_obj.order_status = "On the way"
            order_obj.save()
        elif action == "OCO":
            order_obj.order_status = "Order Completed"
            order_obj.save()
        elif action == "OCA":
            order_obj.order_status = "Order Cancelled"
            order_obj.save()
        else:
            pass
        return redirect('adminHome')

class AdminOrderDetailView(TemplateView):
    template_name="AdminPages/adminOrderDetail.html"
    model = Order

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated and AdminUser.objects.filter(user=self.request.user).exists():
            context = super().get_context_data()
            order_id = self.kwargs["pk"]
            order = Order.objects.get(id=order_id)
            context["ord_obj"]=order
            return context
        else:
            return redirect("/login/?next=/adminpanel/")

class AdminListAllOrders(TemplateView):
    template_name = "AdminPages/adminHome.html"
    model = Order
    def get_context_data(self):
        if self.request.user.is_authenticated and AdminUser.objects.filter(user=self.request.user).exists():
            context = super().get_context_data()
            ListOfOrders = Order.objects.order_by("-created_at")
            context["Orders"]=ListOfOrders
            context["title"]="ALL ORDERS"
            return context
        else:
            return redirect("/adminpanel/login?next=/adminpanel/AllOrders/")

class AdminProductListView(TemplateView):
    template_name = "AdminPages/adminproductlist.html"
    model = Product
    def get_context_data(self):
        if self.request.user.is_authenticated and AdminUser.objects.filter(user=self.request.user).exists():
            context = super().get_context_data()
            allProductList = Product.objects.all().order_by("-view_count")
            context["allproducts"]=allProductList
            return context
        else:
            return redirect("/adminpanel/login?next=/adminpanel/Product-list/")


class AdminProductCreateView(TemplateView):
    template_name = "AdminPages/adminproductpage.html"
    form_class = ProductForm

    def get(self, *args):
        form=ProductForm()
        return render(self.request, self.template_name,{'form':form})
    def post(self, form):
        form = ProductForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            print('valid')
            if self.request.user.is_authenticated and AdminUser.objects.filter(user=self.request.user).exists():
                post=form.save(commit=True)
                return redirect('/adminpanel/Product-list')
        else:
            return render(self.request, self.template_name,{'form':form})

class StaffListView(TemplateView):
    template_name="AdminPages/StaffList.html"
    def get(self, *args):
        if self.request.user.is_authenticated and AdminUser.objects.filter(user=self.request.user).exists():
            StaffUserList = AdminUser.objects.exclude(full_name="Administrator")
            return render(self.request, self.template_name,{'StaffUserList':StaffUserList})
