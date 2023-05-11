from django.shortcuts import render
from django.utils import timezone

from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.permissions import Verify, Password
from apps.api.serializers import SignUpSerializer, ChangePaswordSerializer
from apps.users.models import User, CODE_VERIFIED, DONE, HALF


# Create your views here.
class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
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
    permission_classes = (IsAuthenticated, Verify)

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
        verifies.update(is_confirmed=True)
        if user.auth_status not in [DONE, HALF]:
            user.auth_status = CODE_VERIFIED
            user.save()
        return True


class ChangePasswordView(UpdateAPIView):
    permission_classes = (IsAuthenticated, Password)
    serializer_class = ChangePaswordSerializer
    http_method_names = ['put']

    def get_object(self):
        return self.request.user

    def partial_update(self, request, *args, **kwargs):
        super(ChangePasswordView, self).partial_update(request, *args, **kwargs)

        return Response(
            data={
                "detail": "Updated successfully",
                "auth_status": self.request.user.auth_status,
            }, status=200
        )
