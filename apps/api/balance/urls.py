from django.urls import path
from apps.api.balance.views import *

urlpatterns = [
    path('getBalance/', GetBalanceView.as_view()),
]

