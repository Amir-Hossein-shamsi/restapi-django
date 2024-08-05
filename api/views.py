from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import status
from rest_framework.viewsets  import  ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.response import Response


from .models import Collection, Product
from .serializer import CollectionSerializer, ProductSerializer

#......filter Set of products ......
class ProductFilter(FilterSet):
  class Meta:
    model = Product
    fields = {
      'collection_id': ['exact'],
      'unit_price': ['gt', 'lt']
    }
#.....
#..... Default Pagination....
from rest_framework.pagination import PageNumberPagination
class DefaultPagination(PageNumberPagination):
  page_size = 10
#.......

class CollectionViewSet(ModelViewSet):
    queryset=Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class=CollectionSerializer
    pagination_class=DefaultPagination
    filter_backends=[SearchFilter]
    search_fields = ['title']

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).exists():
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)
    

class ProductViewSet(ModelViewSet):
    serializer_class=ProductSerializer
    queryset=Product.objects.select_related('collection').all()    
    pagination_class=DefaultPagination
    filter_backends=[DjangoFilterBackend,SearchFilter]
    filterset_class=ProductFilter
    search_fields = ['title','description']

    @method_decorator(cache_page(5*60))
    def retrieve(self, request, *args, **kwargs):
       return super().retrieve(request, *args, **kwargs)
    
    