from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView

from apps.api.serializers import SignUpSerializer
from apps.users.models import User


# Create your views here.
class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = SignUpSerializer

    def handle_exception(self, exc):
        # call the parent's handle_exception to get the default behavior
        response = super().handle_exception(exc)
        print(response)

        # customize the response message for specific exceptions
        response.data = {"succes": False, "message": response.data}
        response.status_code = status.HTTP_400_BAD_REQUEST

        return response