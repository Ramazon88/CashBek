from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import ErrorDetail
from rest_framework.views import exception_handler

class CustomError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid input.'
    default_code = 'invalid'