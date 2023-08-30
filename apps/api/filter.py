from django_filters import rest_framework as filters

from apps.main.models import Products


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class ProductFilter(filters.FilterSet):
    ven = NumberInFilter(field_name='ven', lookup_expr='in')

    class Meta:
        model = Products
        fields = ['id', 'ven']