from rest_framework import serializers

from apps.main.models import Notifications, ReadNot, FAQ


class SetFirebaseSerializer(serializers.Serializer):
    firebase_id = serializers.CharField(required=True, error_messages={
        'required': 'firebase_id is required'
    })


class GetNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ["id", "created_at", "title_uz", "title_ru", "body_uz", "body_ru", "image"]


class GetReadNotifSerializer(serializers.ModelSerializer):
    notification = GetNotificationsSerializer()

    class Meta:
        model = ReadNot
        fields = ["read", "notification"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data2 = data["notification"]
        data2.update({"read": data["read"]})
        return data2


class GetNotificationsSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ["id", "created_at", "title_uz", "title_ru", "body_uz", "body_ru", "image"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        suucess = {"success": True}
        data.update({"read": True})
        suucess.update(data)
        return suucess


class GetFaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ["id", "question_uz", "question_ru", "answer_uz", "answer_ru"]

