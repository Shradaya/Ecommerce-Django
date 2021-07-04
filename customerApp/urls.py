
from django.conf.urls import url
from .views import *
from django.urls import path


urlpatterns = [
    path("", CustomerProfileView.as_view(), name="customerprofile"),
    path("order-<int:pk>/", CustomerOrderDetailView.as_view(),
         name="customerorderdetail"),
    ]

