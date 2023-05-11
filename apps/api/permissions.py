from rest_framework.permissions import BasePermission


class Verify(BasePermission):
    message = {'success': False,
               'message': "No such user exists"}

    def has_permission(self, request, view):
        return bool(request.user and request.user.auth_status in ['new', 'half_done', 'done'])


class Password(BasePermission):
    message = {'success': False,
               'message': "No such user exists"}

    def has_permission(self, request, view):
        return bool(request.user and request.user.auth_status in ['code_verified', 'half_done', 'done'])