from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('login/', signin, name="signin"),
    path('products/', products, name="products"),
    path('examples/<str:type>', export_example, name="export_example"),
    path('import_products/', import_products, name="import_products"),
    path('export_products/', export_products, name="export_products"),
    path('confirm_products/', confirm_products, name="confirm_products"),
    path('promo/', promo, name="promo"),
    path('import_promo/', import_promo, name="import_promo"),
    path('confirm_promo/', confirm_promo, name="confirm_promo"),
    path('export_promo/<int:pk>', export_promo, name="export_promo"),
    path('asd', confirm_status, name="confirm_status"),
    path('cashbek/', cashbek, name="cashbek"),
    path('shop/', shop, name="shop"),
    path('shop/<int:pk>', shop_detail, name="shop_detail"),
    path('seller_paid/', seller_aggrement, name="seller_paid"),
    path('vendor_paid/', vendor_aggrement, name="vendor_paid"),
    path('seller_paid/<int:pk>/', seller_aggrement_detail, name="seller_paid_detail"),
    path('vendor_paid/<int:pk>/', vendor_aggrement_detail, name="vendor_paid_detail"),
    path('vendor_payment/', vendor_detail, name="vendor_payment"),
]