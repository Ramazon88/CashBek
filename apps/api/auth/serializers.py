import datetime

import requests
from django.contrib.auth.models import update_last_login
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import AccessToken
from apps.api.exceptions import CustomError
from apps.api.utilty import check_phone, send_sms
from apps.users.models import User, NEW, UserConfirmation, HALF, USER, SimpleUsers, DONE
from config.settings import CLIENT_ID, CLIENT_SECRET, MY_ID_URL, error_bot


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
        user = User.objects.filter(Q(phone=validated_data['phone']) & Q(user_type=USER))
        if user.exists():
            if validated_data['phone'] in ["998905555555", "998922222222"]:
                user.first().create_verify_code_demo()
                user.first().save()
                return user.first()
            code = user.first().create_verify_code()
            send_sms(user.first().phone, code)
            user.first().save()
            return user.first()
        user = super(SignUpSerializer, self).create(validated_data)
        if validated_data['phone'] in ["998905555555", "998922222222"]:
            user.create_verify_code_demo()
            user.save()
            return user
        code = user.create_verify_code()
        send_sms(user.phone, code)
        user.save()
        return user

    def validate_phone_number(self, value):
        check_phone(value)
        query = Q(phone=value) & (
                Q(auth_status=NEW) & Q(user_type=USER)
        )
        user = User.objects.filter(query)
        if user.exists():
            if UserConfirmation.objects.filter(user=user.first(), expiration_time__gte=timezone.now(),
                                               is_confirmed=False).exists():
                data = {
                    "code": "102",
                    "message": _("The previous verification code has not expired")
                }
                raise CustomError(data)
            else:
                user.first().delete()

        return value

    def to_representation(self, instance):
        data = {'success': True}
        return data


class VerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(write_only=True, required=True, error_messages={
        'required': 'phone_number is required'
    })
    code = serializers.CharField(write_only=True, required=True, error_messages={
        'required': 'code is required'
    })

    def validate_phone_number(self, phone):
        check_phone(phone)
        return phone


class CreateSimpleUserSerializers(serializers.ModelSerializer):
    code = serializers.CharField(required=True)
    class Meta:
        model = SimpleUsers
        fields = "__all__"

    def create(self, validated_data):
        user = self.context['request'].user
        if user.simple_user:
            raise CustomError({"code": "116", "message": "Already registered with MyID"})
        body = {
            "grant_type": "authorization_code",
            "code": validated_data["code"],
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
        response_access = requests.post(url=MY_ID_URL + "/api/v1/oauth2/access-token", data=body)
        if response_access.status_code == 200:
            header = {
                "Authorization": f"Bearer {response_access.json()['access_token']}"
            }
            response_info = requests.get(url=MY_ID_URL + "/api/v1/users/me", headers=header)
            if response_info.status_code == 200:
                info = response_info.json()
                adress = response_info.json()["profile"]["address"]
                if SimpleUsers.objects.filter(pinfl=info["profile"]["common_data"]["pinfl"]).exists():
                    raise CustomError({"code": "113", "message": "This PINFL user is already registered"})
                data = {'first_name': info["profile"]["common_data"]["first_name"],
                        'last_name': info["profile"]["common_data"]["last_name"],
                        'middle_name': info["profile"]["common_data"]["middle_name"],
                        'passport_number': info["profile"]["doc_data"]["pass_data"],
                        'pinfl': info["profile"]["common_data"]["pinfl"],
                        'birth_date': datetime.datetime.strptime(info["profile"]["common_data"]["birth_date"], "%d.%m.%Y").date(),
                        'gender': "M" if info["profile"]["common_data"]["gender"] == "1" else "F",
                        'birth_place': info["profile"]["common_data"]["birth_place"],
                        'address': f'{adress["permanent_registration"]["region"]} {adress["permanent_registration"]["district"]} {adress["permanent_address"]}' if adress[
                            "permanent_address"] else f'{adress["temporary_registration"]["region"]} {adress["temporary_registration"]["district"]} {adress["temporary_address"]}' if
                        adress["temporary_address"] else "",
                        }
                obj = super().create(data)
                user.simple_user = obj
                user.auth_status = DONE
                user.save()
                return obj
            else:
                raise CustomError({"code": "118", "message": "My ID error"})
        else:
            raise CustomError({"code": "118", "message": "My ID error"})


    def to_representation(self, instance):
        data = {
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'middle_name': instance.middle_name,
            'phone': instance.simple_user.phone,
            'passport_number': instance.passport_number,
            'pinfl': instance.pinfl,
            'birth_date': instance.birth_date,
            'gender': instance.gender,
            'birth_place': instance.birth_place,
            'address': instance.address,
        }
        return {"success": True, "auth_status": DONE, "result": data}


class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        access_token_instance = AccessToken(data['access'])
        user_id = access_token_instance['user_id']
        user = get_object_or_404(User, id=user_id)
        update_last_login(None, user)
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

# class ChangePasswordSerializer(serializers.Serializer):
#     password = serializers.CharField(write_only=True, required=True, error_messages={
#         'required': 'password is required'
#     })
#     confirm_password = serializers.CharField(write_only=True, required=True, error_messages={
#         'required': 'confirm_password is required'
#     })
#
#     def validate_password(self, password):
#         validate_password(password)
#         return password
#
#     def validate(self, data):
#         password = data.get('password')
#         confirm_password = data.get('confirm_password')
#         if password:
#             validate_password(password)
#         if password != confirm_password:
#             raise CustomError({"code": "108", "message": "Your passwords don't match"})
#
#         return data
#
#     def update(self, instance, validated_data):
#         instance.username = validated_data.get('username', instance.username)
#         instance.password = validated_data.get('password', instance.password)
#         if validated_data.get('password'):
#             instance.set_password(validated_data.get('password'))
#         if instance.auth_status == CODE_VERIFIED:
#             user = self.context['request'].user
#             user.auth_status = HALF
#             user.save()
#         instance.save()
#         return instance
#
#     def to_representation(self, instance):
#         return {"success": True,
#                 "auth_status": instance.auth_status,
#                 }
#
#
# class LoginSerializer(TokenObtainPairSerializer):
#     default_error_messages = {
#         "no_active_account": OrderedDict([("message", _("No active account found with the given credentials"))])
#     }
#
#
# class ForgotPasswordSerializers(serializers.Serializer):
#
#     def __init__(self, *args, **kwargs):
#         super(ForgotPasswordSerializers, self).__init__(*args, **kwargs)
#         self.fields['phone_number'] = serializers.CharField(required=True, error_messages={
#             'required': 'phone_number is required'
#         })
#
#     def validate_phone_number(self, value):
#         check_phone(value)
#         return value
#
#
# class ForgotPasswordVerifySerializers(serializers.Serializer):
#
#     def __init__(self, *args, **kwargs):
#         super(ForgotPasswordVerifySerializers, self).__init__(*args, **kwargs)
#         self.fields['phone_number'] = serializers.CharField(required=True, error_messages={
#             'required': 'phone_number is required'
#         })
#         self.fields['code'] = serializers.CharField(required=True, error_messages={
#             'required': 'code is required'
#         })
#
#     def validate_phone_number(self, value):
#         check_phone(value)
#         return value
