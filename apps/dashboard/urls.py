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
]