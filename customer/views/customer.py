from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from setup.views import BaseModelViewSet
from setup.permissions import IsCustomer

from product.models import Variant
from product.models import Collection
from product.models import LookBook
from masterdata.models import Category
from customer.models import Return

from product.serializers import VariantModelSerializerGET
from product.serializers import CollectionModelSerializerGET
from product.serializers import LookBookModelSerializerGET
from masterdata.serializers import CategoryModelSerializer
from customer.serializers import ReturnModelSerializer
from customer.serializers import ReturnModelSerializerGET
from customer.serializers import ReturnTrackingUpdateSerializer

from customer.filters import CustomerVariantFilter
from customer.filters import CustomerCategoryFilter
from customer.filters import CustomerCollectionFilter
from customer.filters import CustomerLookBookFilter
from customer.filters import CustomerReturnFilter


class CustomerVariantViewSet(GenericViewSet, ListModelMixin):
    permission_classes = (AllowAny,)
    queryset = Variant.objects.all()
    serializer_class = VariantModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerVariantFilter
    search_fields = ['product__name', 'product__brand', 'product__tags']


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


class CustomerReturnViewSet(BaseModelViewSet):
    permission_classes = (IsAuthenticated, IsCustomer,)
    queryset = Return.objects.all()
    serializer_class = ReturnTrackingUpdateSerializer
    retrieve_serializer_class = ReturnModelSerializerGET
    filterset_class = CustomerReturnFilter
    search_fields = ['reason__title', 'product__product__name', 'refund_method', 'status', 'refund_status']

    @action(detail=False, methods=['POST'], url_path='add-return', serializer_class=ReturnModelSerializer)
    def create_record(self, request, *args, **kwargs):
        serializer = ReturnModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Successfully added return request.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)



