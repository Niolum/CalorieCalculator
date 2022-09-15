import django_filters
from django_filters import CharFilter
from .models import Product


class ProductFilter(django_filters.FilterSet):
    product_name = CharFilter(field_name='name', lookup_expr='icontains', label='search product items')

    class Meta:
        model = Product
        fields = ['product_name']