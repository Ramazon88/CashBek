from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from apps.users.models import USER, DONE, HALF


class MyID(BasePermission):
    message = {'code': '106',
               'message': "No such user exists"}

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.user_type == USER and request.user.auth_status in [
                HALF, DONE] and request.user.is_active)


class CustomIsAuthenticated(IsAuthenticated):
    message = {'code': '106',
               'message': "No such user exists"}


class UserPermission(BasePermission):
    message = {'code': '106',
               'message': "No such user exists"}

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.user_type == USER and request.user.auth_status in [
                DONE] and request.user.is_active)
