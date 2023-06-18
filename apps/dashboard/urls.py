from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('products/', products, name="products"),
    path('products/examples/', export_example, name="export_example"),
    path('products/import_products/', import_products, name="import_products"),
    path('products/export_products/', export_products, name="export_products"),
    path('products/confirm_products/', confirm_products, name="confirm_products"),
]