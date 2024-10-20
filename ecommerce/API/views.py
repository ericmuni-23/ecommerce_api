from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Product
from .serializers import ProductSerializer
from .filters import ProductFilter
from .pagination import StandardResultsPagination

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'category__name']
    