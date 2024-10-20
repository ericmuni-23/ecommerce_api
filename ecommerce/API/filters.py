from django_filters import rest_framework as filters
from ..models import Product

class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    category = filters.NumberFilter(field_name='category__id')
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    in_stock = filters.BooleanFilter(method='filter_in_stock')

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock_quantity__gt=0)
        return queryset

    class Meta:
        model = Product
        fields = ['name', 'category', 'min_price', 'max_price', 'in_stock']
