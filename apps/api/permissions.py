from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class Verify(BasePermission):
    message = {'code': '106',
               'message': "No such user exists"}

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.user_type == "user")


class Password(BasePermission):
    message = {'code': '106',
               'message': "No such user exists"}

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.user_type == "user" and request.user.auth_status in [
                'code_verified', 'half_done', 'done'])


class CustomIsAuthenticated(IsAuthenticated):
    message = {'code': '106',
               'message': "No such user exists"}


class UserPermission(BasePermission):
    message = {'code': '106',
               'message': "No such user exists"}

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.user_type == "user")
