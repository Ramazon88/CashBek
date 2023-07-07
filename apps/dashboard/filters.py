import django_filters

from apps.main.models import Products


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Products
        fields = ['is_active', 'vendor__vendor', 'datetime']
