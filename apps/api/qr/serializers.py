from django.utils import timezone
from rest_framework import serializers

from apps.api.exceptions import CustomError
from apps.main.models import QR_code, Token_confirm


class GetTokenSerializer(serializers.Serializer):
    qr_id = serializers.CharField(required=True, error_messages={
        'required': 'qr_id is required'
    })

    def validate_qr_id(self, value):
        now = timezone.now()
        qr = QR_code.objects.filter(qr_id=value, is_used=False, expiry_date__gt=now)
        if qr.exists():
            return value
        else:
            data = {
                'code': '119',
                'message': "QR code is incorrect or expired"
            }
            raise CustomError(data)


class CashbekSerializer(serializers.Serializer):
    token_id = serializers.CharField(required=True, error_messages={
        'required': 'qr_id is required'
    })
    amount = serializers.IntegerField(required=False)

    def validate_token_id(self, value):
        now = timezone.now()
        token = Token_confirm.objects.filter(token=value, is_used=False, expiry_date__gt=now)
        if token.exists():
            return value
        else:
            data = {
                'code': '120',
                'message': "Token is incorrect or expired"
            }
            raise CustomError(data)