from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from rest_framework.permissions import AllowAny

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

# from algoliasearch_django import raw_search

from product.models import Variant
from product.models import Collection
from product.models import LookBook
from masterdata.models import Category

from product.serializers import VariantModelSerializerGET
from product.serializers import CollectionModelSerializerGET
from product.serializers import LookBookModelSerializerGET
from masterdata.serializers import CategoryModelSerializer

from customer.filters import CustomerVariantFilter
from customer.filters import CustomerCategoryFilter
from customer.filters import CustomerCollectionFilter
from customer.filters import CustomerLookBookFilter


class CustomerVariantViewSet(GenericViewSet, ListModelMixin):
    permission_classes = (AllowAny,)
    queryset = Variant.objects.all()
    serializer_class = VariantModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerVariantFilter
    search_fields = ['product__name', 'product__brand', 'product__tags']

    # def list(self, request, *args, **kwargs):
    #     query = request.query_params.get('query', '')
    #     search_results = raw_search(Variant, query)  # Query Algolia index
    #     serializer = self.get_serializer(search_results, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerCategoryViewSet(GenericViewSet, ListModelMixin):
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerCategoryFilter
    search_fields = ['name', 'tags', 'handle']


class CustomerCollectionViewSet(GenericViewSet, ListModelMixin):
    permission_classes = (AllowAny,)
    queryset = Collection.objects.all()
    serializer_class = CollectionModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerCollectionFilter
    search_fields = ['name', 'tags', 'description']


class CustomerLookBookViewSet(GenericViewSet, ListModelMixin):
    permission_classes = (AllowAny,)
    queryset = LookBook.objects.all()
    serializer_class = LookBookModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerLookBookFilter
    search_fields = ['name']



