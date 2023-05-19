from django.urls import path
from apps.api.views import *

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('sign/', CreateUserView.as_view()),
    path('verify/', VerifyApiView.as_view()),
    path('changePassword/', ChangePasswordView.as_view()),
    path('forgotPassword/', ForgotPasswordView.as_view()),
    path('forgotPasswordVerify/', ForgotPasswordVerifyView.as_view()),
    path('logout/', LogoutView.as_view())
]

