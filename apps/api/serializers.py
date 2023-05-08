from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.api.utilty import check_phone, send_sms
from apps.users.models import User, NEW, CODE_VERIFIED


class SignUpSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)
        self.fields['phone_number'] = serializers.CharField(required=True, source="phone")

    class Meta:
        model = User
        fields = (
            "auth_status",
        )
        extra_kwargs = {
            'auth_status': {'read_only': True, 'required': False},
            'phone_number': {"error_messages": {"required": "Give yourself a username"}}
        }

    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        code = user.create_verify_code()
        send_sms(user.phone, code)
        user.save()
        return user

    def validate_phone_number(self, value):
        check_phone(value)
        query = Q(phone=value) & (
                Q(auth_status=NEW) | Q(auth_status=CODE_VERIFIED)
        )

        # if User.objects.filter(query).exists():
        #     User.objects.get(query).delete()

        if value and User.objects.filter(phone=value).exists():
            data = {
                "success": False,
                "message": _("This phone is already being used!")
            }
            raise ValidationError(data)

        return value

    def to_representation(self, instance):
        data = super(SignUpSerializer, self).to_representation(instance)
        data.update(instance.tokens())
        return data
