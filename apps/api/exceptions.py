from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import status
from rest_framework import exceptions
from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response
from rest_framework.views import exception_handler, set_rollback


class CustomError(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid input.'
    default_code = 'invalid'


def custom_exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    data = {"success": False}
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    if isinstance(exc, exceptions.APIException):
        print(exc)
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if exc.default_code == "token_not_valid":
            data.update({"code": "104", "message": "Given token not valid for any token type"})
            return Response(data=data, status=401)
        elif exc.default_code == "not_authenticated":
            data.update({"code": "110", "message": "Authentication credentials were not provided"})
            return Response(data=data, status=401)
        elif exc.default_code == "permission_denied":
            data.update({"code": "111", "message": "Permission denied"})
            return Response(data=data, status=403)
        elif exc.default_code == "authentication_failed":
            data.update({"code": "112", "message": "User not found"})
            return Response(data=data, status=401)
        elif isinstance(exc, CustomError):
            data.update(exc.detail)
            return Response(data=data, status=400)
        elif isinstance(exc, exceptions.ValidationError):
            if exc.detail.get("password") and exc.detail.get("password")[0].code != "required":
                data.update({"code": "107"})
                data.update(exc.detail)
                return Response(data=data, status=400)
            elif exc.detail.get("pinfl") and exc.detail.get("pinfl")[0].code != "required":
                data.update({"code": "113", "message": "This PINFL user is already registered"})
                return Response(data=data, status=400)
            else:
                data.update({"code": "101"})
                data.update(exc.detail)
                return Response(data=data, status=400)

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'detail': exc.detail}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None
