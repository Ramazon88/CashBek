import django_filters

from apps.main.models import *


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Products
        fields = ['is_active', 'vendor__vendor']


class PromoFilter(django_filters.FilterSet):
    class Meta:
        model = Promo
        fields = ['status', 'vendor__vendor']
