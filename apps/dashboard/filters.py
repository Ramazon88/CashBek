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