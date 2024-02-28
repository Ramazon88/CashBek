from django.urls import path
from apps.api.auth.views import *

urlpatterns = [
    path('sign/', CreateUserView.as_view(), name='Sign in'),
    path('changePhone/', ChangePhoneView.as_view()),
    path('changePhoneVerify/', ChangePhoneVerifyApiView.as_view()),
    # path('login/', LoginView.as_view(), name='Login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='Refresh token'),
    path('verify/', VerifyApiView.as_view(), name='Send verify code for sign in'),
    # path('newVerify/', GetNewVerification.as_view(), name='Send again verify code'),
    # path('changePassword/', ChangePasswordView.as_view(), name='Set or change password'),
    # path('forgotPassword/', ForgotPasswordView.as_view(), name='Send phone number for repair password'),
    # path('forgotPasswordVerify/', ForgotPasswordVerifyView.as_view(), name='Send verify code for repair password'),
    path('setUserInfo/', CreateSimpleUserView.as_view(), name='Set MyID INFO'),
    path('getUserInfo/', GetUserInfoView.as_view(), name='Get MyID INFO'),
    path('setUserPhoto/', SetUserPhotoView.as_view()),
    path('logout/', LogoutView.as_view(), name='Logout'),
    path('getVerifyDeleteUser/', GetDeleteVerify.as_view()),
    path('confirmDeleteUser/', ConfirmDeleteUserView.as_view()),
    path('checkAvailableUserByPass/', CheckAvailableUserByPassView.as_view()),
]

