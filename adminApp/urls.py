from django.conf.urls import url
from .views import *
from django.urls import path


urlpatterns = [
    path("", adminHomePage.as_view(), name="adminHome"),
    path("login/", adminLogin.as_view(), name="adminlogin"),
    path("manage-cart/<int:o_id>/", ManageOrder.as_view(), name="manageorder"),
    path("order-<int:pk>/", AdminOrderDetailView.as_view(),name="adminOrderDetailView"),
    path("AllOrders/", AdminListAllOrders.as_view(), name="adminallorderslist"),
    path("Product-list/", AdminProductListView.as_view(), name="adminproductlist"),
    path("Product-add/", AdminProductCreateView.as_view(), name="adminproductcreate"),
    path("Staff-List/", StaffListView.as_view(), name="stafflist"),
    path("messages/",messages.as_view(), name="viewmessages"),
]

