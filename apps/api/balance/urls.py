from django.urls import path
from apps.api.balance.views import *

urlpatterns = [
    path('getBalance/', GetBalanceView.as_view()),
    path('getCheck/', GetCheckView.as_view()),
    path('getAllBalance/', GetAllBalanceView.as_view()),
    path('getProducts/', GetProductsView.as_view()),
]

