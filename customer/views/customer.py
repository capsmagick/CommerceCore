from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

from rest_framework import filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend


# from algoliasearch_django import raw_search

from product.models import Products
from product.models import Variant
from product.models import Collection
from product.models import LookBook
from masterdata.models import Category
from orders.models import Order

from product.serializers import ProductsModelSerializerGET
from product.serializers import VariantModelSerializerGET
from product.serializers import CollectionModelSerializerGET
from product.serializers import LookBookModelSerializerGET
from orders.serializers import OrderItemsModelSerializerGET

from masterdata.serializers import CategoryModelSerializerGET

from customer.filters import CustomerProductFilter
from customer.filters import CustomerVariantFilter
from customer.filters import CustomerCategoryFilter
from customer.filters import CustomerCollectionFilter
from customer.filters import CustomerLookBookFilter
from customer.filters import CustomerOrderFilter


class CustomerProductViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
        Get the list of variant products.

        Parameters:
            request (HttpRequest): The HTTP request object containing model data.

        Returns:
            Response: A DRF Response object with the variant product data.
    """
    permission_classes = (AllowAny,)
    queryset = Products.objects.all()
    serializer_class = ProductsModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerProductFilter
    search_fields = ['name', 'brand']

    @action(detail=True, methods=['GET'], url_path='other-variants')
    def other_variants(self, request, *args, **kwargs):
        """
            API to fetch all similar variants
        """
        obj = self.get_object()
        return Response(
            VariantModelSerializerGET(obj.product_variant.all(), many=True).data,
            status=status.HTTP_200_OK
        )


class CustomerVariantViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    """
        Get the list of variant products.

        Parameters:
            request (HttpRequest): The HTTP request object containing model data.

        Returns:
            Response: A DRF Response object with the variant product data.
    """
    permission_classes = (AllowAny,)
    queryset = Variant.objects.filter(product__deleted=False)
    serializer_class = VariantModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerVariantFilter
    search_fields = ['product__name', 'product__brand', 'product__tags']

    @action(detail=True, methods=['GET'], url_path='other-variants')
    def other_variants(self, request, *args, **kwargs):
        """
            API to fetch all similar variants
        """
        obj = self.get_object()
        return Response(
            VariantModelSerializerGET(obj.product.product_variant.all(), many=True).data,
            status=status.HTTP_200_OK
        )

    # def list(self, request, *args, **kwargs):
    #     query = request.query_params.get('query', '')
    #     search_results = raw_search(Variant, query)  # Query Algolia index
    #     serializer = self.get_serializer(search_results, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerCategoryViewSet(GenericViewSet, ListModelMixin):
    """
        Get the list of categories.

        Parameters:
            request (HttpRequest): The HTTP request object containing model data.

        Returns:
            Response: A DRF Response object with the category data.
    """

    permission_classes = (AllowAny,)
    queryset = Category.objects.filter(parent_category__isnull=True).order_by('name')
    serializer_class = CategoryModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerCategoryFilter
    search_fields = ['name', 'tags', 'handle']


class CustomerCollectionViewSet(GenericViewSet, ListModelMixin):
    """
        Get the list of collection.

        Parameters:
            request (HttpRequest): The HTTP request object containing model data.

        Returns:
            Response: A DRF Response object with the collection data.
    """
    permission_classes = (AllowAny,)
    queryset = Collection.objects.all()
    serializer_class = CollectionModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerCollectionFilter
    search_fields = ['name', 'tags', 'description']


class CustomerLookBookViewSet(GenericViewSet, ListModelMixin):
    """
        Get the list of look book.

        Parameters:
            request (HttpRequest): The HTTP request object containing model data.

        Returns:
            Response: A DRF Response object with the look book data.
    """
    permission_classes = (AllowAny,)
    queryset = LookBook.objects.all()
    serializer_class = LookBookModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerLookBookFilter
    search_fields = ['name']


class CustomerOrderViewSet(GenericViewSet, ListModelMixin):
    """
        Get the list of Orders.

        Parameters:
            request (HttpRequest): The HTTP request object containing model data.

        Returns:
            Response: A DRF Response object with the look book data.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderItemsModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerOrderFilter
    search_fields = ['order_id']

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user.username)
