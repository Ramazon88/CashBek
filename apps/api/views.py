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
from apps.api.permissions import Verify, Password, CustomIsAuthenticated, UserPermission
from apps.api.serializers import SignUpSerializer, ChangePasswordSerializer, LogoutSerializer, LoginSerializer, \
    CustomTokenRefreshSerializer
from apps.api.utilty import check_phone, send_sms
from apps.users.models import User, CODE_VERIFIED, DONE, HALF, UserConfirmation


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

    def handle_exception(self, exc):
        # call the parent's handle_exception to get the default behavior
        response = super().handle_exception(exc)
        if isinstance(exc, ValidationError):
            # customize the response message for specific exceptions
            response.data = {"succes": "False", "message": response.data["phone_number"][0]}
            response.status_code = status.HTTP_400_BAD_REQUEST

            return response
        else:
            response.data = {"succes": "False", "message": response.data['message']}
            return response


class VerifyApiView(APIView):
    permission_classes = (CustomIsAuthenticated, Verify, UserPermission)

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        data = {"success": "False"}
        if exc.default_code == "token_not_valid":
            data.update({"message": "Given token not valid for any token type"})
            return Response(data=data, status=401)
        return response

    def post(self, request, *args, **kwargs):
        user, code = self.request.user, self.request.data.get('code')
        self.check_verify(user, code)
        token = user.tokens()
        return Response(
            data={
                "success": "True",
                "auth_status": user.auth_status,
                "access": token["access"],
                "refresh": token["refresh"]
            }, status=200)

    @staticmethod
    def check_verify(user, code):
        verifies = user.verify_codes.filter(expiration_time__gte=timezone.now(), code=code, is_confirmed=False)
        if not verifies.exists():
            data = {
                'success': 'False',
                'message': "Code is incorrect or expired"
            }
            raise ValidationError(data)
        verifies.delete()
        if user.auth_status not in [DONE, HALF]:
            user.auth_status = CODE_VERIFIED
            user.save()
        return True


class ChangePasswordView(UpdateAPIView):
    permission_classes = (CustomIsAuthenticated, Password, UserPermission)
    serializer_class = ChangePasswordSerializer
    http_method_names = ['put']

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        data = {"success": "False"}
        if exc.default_code == "token_not_valid":
            data.update({"message": "Given token not valid for any token type"})
            return Response(data=data, status=401)
        data.update(dict(response.data))
        return Response(data=data, status=400)

    def get_object(self):
        return self.request.user


class LogoutView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (CustomIsAuthenticated, UserPermission)

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        data = {"success": "False"}
        if exc.default_code == "token_not_valid":
            data.update({"message": "Given token not valid for any token type"})
            return Response(data=data, status=401)
        return response

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                'success': "True",
                "message": "You are logged out"
            }
            return Response(data=data, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response(data={"success": "False", "message": "this token is not available"},
                            status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        data = {"success": "True"}
        data.update(serializer.validated_data)

        return Response(data, status=status.HTTP_200_OK)


class CustomTokenRefreshView(TokenObtainPairView):
    serializer_class = CustomTokenRefreshSerializer

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        data = {"success": "False"}
        if exc.default_code == "token_not_valid":
            data.update({"message": "Given token not valid for any token type"})
            return Response(data=data, status=401)
        return response

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        data = {"success": "True"}
        data.update(serializer.validated_data)

        return Response(data, status=status.HTTP_200_OK)


class GetNewVerification(APIView):
    permission_classes = (CustomIsAuthenticated, UserPermission)

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        data = {"success": "False"}
        if exc.default_code == "token_not_valid":
            data.update({"message": "Given token not valid for any token type"})
            return Response(data=data, status=401)
        return response

    def get(self, request, *args, **kwargs):
        user = self.request.user
        self.check_verification(user)
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
                "message": "You need to wait over expiration time",
            }
            raise ValidationError(data)


class ForgotPasswordView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            phone = request.data["phone"]
        except:
            return Response({"success": "False", "message": "phone is required"}, status=400)
        query = Q(phone=phone) & Q(user_type="user") & (
                Q(auth_status=HALF) | Q(auth_status=DONE)
        )
        user = User.objects.filter(query)
        if user.exists():
            UserConfirmation.objects.filter(user=user.first(), expiration_time__gte=timezone.now()).delete()
            code = user.first().create_verify_code()
            send_sms(phone, code)
            return Response({"success": "True"}, status=200)
        else:
            return Response({"success": "False", "message": "No such user exists"}, status=400)


class ForgotPasswordVerifyView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            phone = request.data["phone"]
            code = request.data["code"]
        except:
            return Response({"success": "False", "message": "phone or code is required"}, status=400)

        query = Q(phone=phone) & Q(user_type="user") & (
                Q(auth_status=HALF) | Q(auth_status=DONE)
        )
        user = User.objects.filter(query)
        if user.exists():
            self.check_verify(user.first(), code)
            token = user.first().tokens()
            return Response({"success": "True",
                             "refresh": token["refresh"],
                             "access": token["access"]}, status=200)
        else:
            return Response({"success": "False", "message": "No such user exists"}, status=400)

    @staticmethod
    def check_verify(user, code):
        verifies = user.verify_codes.filter(expiration_time__gte=timezone.now(), code=code, is_confirmed=False)
        if not verifies.exists():
            data = {
                'success': 'False',
                'message': "Code is incorrect or expired"
            }
            raise ValidationError(data)
        verifies.delete()
        return True