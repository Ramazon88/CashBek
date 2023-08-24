from rest_framework.views import APIView

from apps.api.permissions import UserPermission


class GetBalanceView(APIView):
    permission_classes = (UserPermission,)
