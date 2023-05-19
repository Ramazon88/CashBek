import datetime
from collections import OrderedDict

from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import AccessToken

from apps.api.exceptions import CustomError
from apps.api.utilty import check_phone, send_sms
from apps.users.models import User, NEW, CODE_VERIFIED, UserConfirmation, HALF


class SignUpSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(SignUpSerializer, self).__init__(*args, **kwargs)
        self.fields['phone_number'] = serializers.CharField(required=True, source="phone", error_messages={
            'required': 'phone_number is required'
        })

    class Meta:
        model = User
        fields = (
            "auth_status",
        )
        extra_kwargs = {
            'auth_status': {'read_only': True, 'required': False},
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
        user = User.objects.filter(query)
        if user.exists():
            if UserConfirmation.objects.filter(user=user.first(), expiration_time__gte=timezone.now(),
                                               is_confirmed=False).exists():
                data = {
                    "message": _("The previous verification code has not expired")
                }
                raise CustomError(data)
            else:
                user.first().delete()

        if value and User.objects.filter(phone=value).exists():
            data = {
                "message": _("This phone is already being used!")
            }
            raise CustomError(data)

        return value

    def to_representation(self, instance):
        text = super(SignUpSerializer, self).to_representation(instance)
        data = {'succes': "True"}
        data.update(text)
        data.update(instance.tokens())
        return data


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, error_messages={
        'required': 'password is required'
    })
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate_password(self, password):
        validate_password(password)
        return password

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password:
            validate_password(password)
            validate_password(confirm_password)
        if password != confirm_password:
            raise CustomError({"success": "False",
                               "message": "Your passwords don't match"})

        return data

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
        if instance.auth_status == CODE_VERIFIED:
            user = self.context['request'].user
            user.auth_status = HALF
            user.save()
        instance.save()
        return instance

    def to_representation(self, instance):
        return {"success": "True",
                "auth_status": instance.auth_status,
                }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class LoginSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": OrderedDict([("success", False),
                                          ("message", _("No active account found with the given credentials"))])
    }


class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        access_token_instance = AccessToken(data['access'])
        user_id = access_token_instance['user_id']
        user = get_object_or_404(User, id=user_id)
        update_last_login(None, user)
        return data


class ForgotPasswordSerializers(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        super(ForgotPasswordSerializers, self).__init__(*args, **kwargs)
        self.fields['phone_number'] = serializers.CharField(required=True, source="phone", error_messages={
            'required': 'phone_number is required'
        })

    def validate_phone_number(self, value):
        check_phone(value)
        query = Q(phone=value) & (
                Q(auth_status=NEW) | Q(auth_status=CODE_VERIFIED)
        )
        user = User.objects.filter(query)
        if user.exists():
            if UserConfirmation.objects.filter(user=user.first(), expiration_time__gte=timezone.now(),
                                               is_confirmed=False).exists():
                data = {
                    "message": _("The previous verification code has not expired")
                }
                raise CustomError(data)
            else:
                user.first().delete()

        if value and User.objects.filter(phone=value).exists():
            data = {
                "message": _("This phone is already being used!")
            }
            raise CustomError(data)

        return value

    def to_representation(self, instance):
        text = super(ForgotPasswordSerializers, self).to_representation(instance)
        data = {'succes': "True"}
        data.update(text)
        data.update(instance.tokens())
        return data