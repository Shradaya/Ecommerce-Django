from django.shortcuts import render
from django.views.generic import TemplateView, View, CreateView, FormView
from django.core.paginator import Paginator
from .models import *
from customerApp.models import Customer
from django.contrib import messages
from django.shortcuts import redirect
from .forms import *
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from .forms import PostForm
from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone

# Create your views here.
def ContactPage(request):

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.Date = timezone.now()
            post.save()
            messages.success(request, 'Message Sent Successfully')
            return redirect('/contact/')
    else:
        form = PostForm()
    return render(request, 'contact.html', {'form': form})



class HomePage(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = Product.objects.all().order_by("-id")
        if len(all_products)>=3:
            context['product_list'] = all_products[:3]
        else:
            context['product_list']=all_products
        return context

class ProductListPage(TemplateView):
    template_name="product_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = Product.objects.all().order_by("-id")
        paginator = Paginator(all_products, 12)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        return context

class ProductDetailPage(TemplateView):
    template_name="product_detail.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        return context

class AddToCartView(TemplateView):
    template_name = "product_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_products = Product.objects.all().order_by("-id")
        paginator = Paginator(all_products, 12)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Product.objects.get(id=product_id)

        # check if cart exists
        """carts =  Cart.objects.filter(customer=self.request.user.customer)
        last_cart = carts.latest('created_at')
        if Order.objects.get(cart=last_cart):
            cart_id = last_cart.id
        else:
            cart_id = self.request.session.get("cart_id", None)"""
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)


            # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.selling_price
                cartproduct.save()
                cart_obj.total += product_obj.selling_price
                cart_obj.save()
            # new item is added in cart
            else:
                a =  cart_obj.id
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
                cart_obj.total += product_obj.selling_price
                cart_obj.save()


        else:
            cart_obj = Cart.objects.create()
            try:
                if self.request.user.is_authenticated and self.request.user.customer:
                    cart_obj.customer = self.request.user.customer
            except:
                pass
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.selling_price, quantity=1, subtotal=product_obj.selling_price)
            cart_obj.total += product_obj.selling_price
            cart_obj.save()
        self.request.session['CartProduct']=len(CartProduct.objects.filter(cart = cart_obj))
        print(str(len(CartProduct.objects.filter(cart = cart_obj)))+ " Printed Data")


        messages.success(self.request, 'Item '+ product_obj.title +' Added To Cart successfully')
        return context

class MyCartView(TemplateView):
    template_name = "checkout.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj

        form = CheckoutForm()
        context['form']=form
        return context
    def post(self, *args):
        print("*****DONE*****")
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            cart_id = self.request.session.get("cart_id")
            if cart_id:
                cart_obj = Cart.objects.get(id=cart_id)
                form.instance.cart = cart_obj
                form.instance.subtotal = cart_obj.total
                form.instance.discount = 0
                form.instance.total = cart_obj.total
                form.instance.order_status = "Order Received"
                del self.request.session['cart_id']
                pm = form.cleaned_data.get("payment_method")
                order = form.save(commit=True)
                if pm=="Cash On Delivery":
                    print("DONE*****")
                    return redirect('Homepage')
                if pm=="Esewa":
                    return redirect(reverse("esewarequest") + "?o_id=" + str(order.id))
        return redirect('Homepage')


class ManageCartItems(View):
    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs["cp_id"]
        action = request.GET.get("action")
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart

        if action == "inc":
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == "dcr":

            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                self.request.session['CartProduct']-=1
                cp_obj.delete()

        elif action == "del":
            self.request.session['CartProduct']-=1
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect("mycart")


class EmptyCart(View):
    def get(self, request, *args, **kwargs):
        cart_id = request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            self.request.session['CartProduct']=0
            cart.total = 0
            cart.save()
        return redirect("mycart")



def search(request):
    prodict = {'Earring':1}
    products = Product.objects.all()
    if 'a' in request.GET and request.GET['a']:
        a = request.GET['a']
        products = products.filter(title__icontains=a)
    if 'c' in request.GET and request.GET['c']:
        c = request.GET['c']
        products = products.filter(category=prodict['Earring'])
    if 'H' in request.GET and request.GET['H']:
        try:
            H = int(request.GET['H'])
            print(H)
            products = products.filter(selling_price__lte=H)
            print(products)
        except:
            pass
    if 'L' in request.GET and request.GET['L']:
        try:
            L = int(request.GET['L'])
            print(L)
            print(products)
            products = products.filter(selling_price__gte=L)
            print(products)
        except:
            print("failed")
            pass
    return render(request, 'product_list.html', {'product_list':products})


class returnCategory(TemplateView):
    template_name = "product_list.html"
    model = Product
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        cat_id = self.kwargs["det"]
        categor = Product.objects.filter(category=cat_id)
        context["product_list"]=categor
        return context

