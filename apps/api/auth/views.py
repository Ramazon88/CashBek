from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.api.exceptions import CustomError
from apps.api.permissions import Verify, Password, UserPermission, MyID
from apps.api.auth.serializers import SignUpSerializer, ChangePasswordSerializer, LogoutSerializer, LoginSerializer, \
    CustomTokenRefreshSerializer, ForgotPasswordSerializers, ForgotPasswordVerifySerializers, \
    CreateSimpleUserSerializers
from apps.api.utilty import send_sms
from apps.users.models import User, CODE_VERIFIED, DONE, HALF, UserConfirmation, USER, SimpleUsers


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer


class VerifyApiView(APIView):
    permission_classes = (Verify,)

    def post(self, request, *args, **kwargs):
        user, code = self.request.user, self.request.data.get('code')
        self.check_verify(user, code)
        token = user.tokens()
        return Response(
            data={
                "success": True,
                "auth_status": user.auth_status,
                "access": token["access"],
                "refresh": token["refresh"]
            }, status=200)

    @staticmethod
    def check_verify(user, code):
        verifies = user.verify_codes.filter(expiration_time__gte=timezone.now(), code=code, is_confirmed=False)
        if not verifies.exists():
            data = {
                'code': '105',
                'message': "Code is incorrect or expired"
            }
            raise CustomError(data)
        verifies.delete()
        if user.auth_status not in [DONE, HALF]:
            user.auth_status = CODE_VERIFIED
            user.save()
        return True


class ChangePasswordView(UpdateAPIView):
    permission_classes = (Password,)
    serializer_class = ChangePasswordSerializer
    http_method_names = ['put']

    def get_object(self):
        return self.request.user


class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (UserPermission,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                'success': True,
                "message": "You are logged out"
            }
            return Response(data=data, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response(data={"success": False, "code": "117", "message": "This refresh token is not available"},
                            status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        data = {"success": True}
        data.update(serializer.validated_data)

        return Response(data, status=status.HTTP_200_OK)


class CustomTokenRefreshView(TokenObtainPairView):
    serializer_class = CustomTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        data = {"success": True}
        data.update(serializer.validated_data)

        return Response(data, status=status.HTTP_200_OK)


class GetNewVerification(APIView):
    permission_classes = (UserPermission,)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        self.check_verification(user)
        code = user.create_verify_code()
        send_sms(user.phone, code)
        return Response(
            {
                "success": True
            }
        )

    @staticmethod
    def check_verification(user):
        verifies = user.verify_codes.filter(expiration_time__gte=timezone.now(), is_confirmed=False)
        if verifies.exists():
            data = {
                "success": False,
                "code": "102",
                "message": "The previous verification code has not expired",
            }
            raise CustomError(data)


class ForgotPasswordView(GenericAPIView):
    serializer_class = ForgotPasswordSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone = request.data["phone_number"]
            query = Q(phone=phone) & Q(user_type=USER) & (
                    Q(auth_status=HALF) | Q(auth_status=DONE)
            )
            user = User.objects.filter(query)
            if user.exists():
                UserConfirmation.objects.filter(user=user.first(), expiration_time__gte=timezone.now()).delete()
                code = user.first().create_verify_code()
                send_sms(phone, code)
                return Response({"success": True}, status=200)
            else:
                return Response({"success": False, "code": "106", "message": "No such user exists"}, status=400)


class ForgotPasswordVerifyView(GenericAPIView):
    serializer_class = ForgotPasswordVerifySerializers

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone = request.data["phone_number"]
            code = request.data["code"]

            query = Q(phone=phone) & Q(user_type=USER) & (
                    Q(auth_status=HALF) | Q(auth_status=DONE)
            )
            user = User.objects.filter(query)
            if user.exists():
                self.check_verify(user.first(), code)
                token = user.first().tokens()
                return Response({"success": True,
                                 "auth_status": user.first().auth_status,
                                 "refresh": token["refresh"],
                                 "access": token["access"]}, status=200)
            else:
                return Response({"success": False, "code": "106", "message": "No such user exists"}, status=400)

    @staticmethod
    def check_verify(user, code):
        verifies = user.verify_codes.filter(expiration_time__gte=timezone.now(), code=code, is_confirmed=False)
        if not verifies.exists():
            data = {
                "code": "105",
                'message': "Code is incorrect or expired"
            }
            raise CustomError(data)
        verifies.delete()
        return True


class CreateSimpleUserView(CreateAPIView):
    queryset = SimpleUsers.objects.all()
    serializer_class = CreateSimpleUserSerializers
    permission_classes = (MyID,)


class GetUserInfoView(APIView):
    permission_classes = (MyID,)

    def get(self, request):
        user = self.request.user
        data = {}
        if user.simple_user:
            data = {
                'first_name': user.simple_user.first_name,
                'last_name': user.simple_user.last_name,
                'middle_name': user.simple_user.middle_name,
                'phone': user.phone,
                'passport_number': user.simple_user.passport_number,
                'pinfl': user.simple_user.pinfl,
                'birth_date': user.simple_user.birth_date,
                'inn': user.simple_user.inn,
                'gender': user.simple_user.gender,
                'birth_place': user.simple_user.birth_place,
                'address': user.simple_user.address,
            }
        return Response(data={"success": True, "auth_status": user.auth_status, "result": data})
