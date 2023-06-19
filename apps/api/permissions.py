from rest_framework.permissions import BasePermission, IsAuthenticated


class Verify(BasePermission):
    message = {'success': False,
               'code': '106',
               'message': "No such user exists"}

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.user_type == "user")


class Password(BasePermission):
    message = {'success': False,
               'code': '106',
               'message': "No such user exists"}

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.user_type == "user" and request.user.auth_status in [
                'code_verified', 'half_done', 'done'])


class CustomIsAuthenticated(IsAuthenticated):
    message = {'success': False,
               'code': '106',
               'message': "No such user exists"}


class UserPermission(BasePermission):
    message = {'success': False,
               'code': '106',
               'message': "No such user exists"}

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.user_type == "user")
