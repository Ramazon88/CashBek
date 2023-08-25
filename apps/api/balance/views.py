from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.balance.serializers import GetCheckSerializer, GetProductSerializer
from apps.api.balance.service import get_balance, get_all_balance
from apps.api.permissions import UserPermission
from apps.main.models import Cashbek, Products, ACTIVE


class CustomListPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'page': self.page.number,
            'count': self.page.paginator.count,
            'page_size': self.page.paginator.per_page,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


class GetBalanceView(APIView, CustomListPagination):
    permission_classes = (UserPermission,)

    def queryset(self):
        return get_balance(self.request.user)

    def get(self, request):
        queryset = self.queryset()
        results = self.paginate_queryset(queryset, request, view=self)
        data = self.get_paginated_response(results)
        res = {"success": True}
        res.update(data.data)
        return Response(res)


class GetCheckView(ListAPIView):
    serializer_class = GetCheckSerializer
    permission_classes = (UserPermission,)
    pagination_class = CustomListPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ["vendor", "id", "types"]

    def get_queryset(self):
        user = self.request.user.simple_user
        return Cashbek.objects.filter(user=user).order_by("-created_at")

    def get_paginated_response(self, data):
        data = super().get_paginated_response(data)
        res = {"success": True}
        res.update(data.data)
        return Response(res)


class GetAllBalanceView(APIView):
    permission_classes = (UserPermission,)

    def get(self, request):
        if self.request.query_params.get("vendor"):
            obj = get_all_balance(self.request.user, self.request.query_params.get("vendor"))
        else:
            obj = get_all_balance(self.request.user)
        res = {"success": True}
        res.update(obj)
        return Response(res)


class GetProductsView(ListAPIView):
    serializer_class = GetProductSerializer
    permission_classes = (UserPermission,)
    pagination_class = CustomListPagination
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('model',)
    filterset_fields = ["ven", "id"]

    def get_queryset(self):
        return Products.objects.filter(promo__status=ACTIVE, is_active=True).order_by("-datetime")

    def get_paginated_response(self, data):
        data = super().get_paginated_response(data)
        res = {"success": True}
        res.update(data.data)
        return Response(res)
