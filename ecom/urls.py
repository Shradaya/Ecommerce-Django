from django.conf.urls import url
from .views import *
from django.urls import path, include


urlpatterns = [
    path('', HomePage.as_view(), name='Homepage'),

    path('all-products/', ProductListPage.as_view(), name='AllProducts'),
    path("product/<slug:slug>/", ProductDetailPage.as_view(), name="productdetail"),
    path("category/<int:det>", returnCategory.as_view(), name="categorydetail"),

    path("add-to-cart-<int:pro_id>/", AddToCartView.as_view(),name ="addtocart"),
    path("my-cart/", MyCartView.as_view(), name="mycart"),
    path("manage-cart/<int:cp_id>/", ManageCartItems.as_view(), name="managecart"),
    path("empty-cart/", EmptyCart.as_view(), name="emptycart"),

    path('search/', search, name='search')
]

