from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from apps.api.balance.views import CustomListPagination
from apps.api.nf.serializers import SetFirebaseSerializer, GetReadNotifSerializer, GetNotificationsSerializer2, \
    GetFaqSerializer
from apps.api.permissions import UserPermission
from apps.main.models import Fribase, Notifications, FAQ


class SetFirebaseView(GenericAPIView):
    permission_classes = (UserPermission,)

    def post(self, request):
        serializer = SetFirebaseSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        Fribase.objects.create(fr_id=serializer.data.get("firebase_id"), user=self.request.user.simple_user)
        return Response({"success": True}, status=201)


class GetNotificationsView(ListAPIView):
    permission_classes = (UserPermission,)
    serializer_class = GetReadNotifSerializer
    pagination_class = CustomListPagination

    def get_queryset(self):
        return self.request.user.simple_user.readnot_set.all()

    def get_paginated_response(self, data):
        data = super().get_paginated_response(data)
        res = {"success": True}
        res.update(data.data)
        return Response(res)


class GetNotificationsByIdView(RetrieveAPIView):
    permission_classes = (UserPermission,)
    serializer_class = GetNotificationsSerializer2

    def get_queryset(self):
        return Notifications.objects.all()

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        read = obj.read.get(user=self.request.user.simple_user)
        read.read = True
        read.save()
        return super().get(request, *args, **kwargs)


class GetFaqView(ListAPIView):
    serializer_class = GetFaqSerializer
    queryset = FAQ.objects.all()

    # def finalize_response(self, request, response, *args, **kwargs):
    #     if response.status_code == 200:
    #         print(response.data)
    #         return Response(data={"success": True, "faq": list(response.data)})
    #     else:
    #         pass
    #     return super().finalize_response(request, response, *args, **kwargs)



