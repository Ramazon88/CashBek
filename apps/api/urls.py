from django.urls import path, include

from apps.api.views import *

urlpatterns = [
    path('sign/', CreateUserView.as_view()),
    path('verify/', VerifyApiView.as_view()),
    path('changepassword/', ChangePasswordView.as_view())
]