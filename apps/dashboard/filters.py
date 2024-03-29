import django_filters
from django import forms

from apps.main.models import *


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Products
        fields = ['is_active', 'vendor__vendor']


class PromoFilter(django_filters.FilterSet):
    class Meta:
        model = Promo
        fields = ['status', 'vendor__vendor']


class CashbekFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')

    class Meta:
        model = Cashbek
        fields = ['vendor', 'types', 'active']


class SellerFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='cash_seller__created_at', lookup_expr='date__gte')
    end_date = django_filters.DateFilter(field_name='cash_seller__created_at', lookup_expr='date__lte')

    class Meta:
        model = Seller
        fields = ['cash_seller__types', 'cash_seller__vendor', 'name']


class PaymentSeller(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')

    class Meta:
        model = PaymentForSeller
        fields = ['created_at']


class PaymentVendor(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='date__gte')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='date__lte')

    class Meta:
        model = PaymentOfVendor
        fields = ['created_at']
