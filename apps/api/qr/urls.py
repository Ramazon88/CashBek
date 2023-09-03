from django.urls import path
from apps.api.qr.views import *

urlpatterns = [
    path('token/', TokenView.as_view()),
    path('cashbek/', CashbekView.as_view()),
]

