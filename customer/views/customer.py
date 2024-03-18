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
from masterdata.models import Category
from customer.models import Return

from product.serializers import VariantModelSerializerGET
from masterdata.serializers import CategoryModelSerializer
from customer.serializers import ReturnModelSerializer
from customer.serializers import ReturnModelSerializerGET
from customer.serializers import ReturnTrackingUpdateSerializer


class CustomerVariantViewSet(GenericViewSet, ListModelMixin):
    permission_classes = (AllowAny,)
    queryset = Variant.objects.all()
    serializer_class = VariantModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['product__name', 'product__brand', 'product__tags']


class CustomerCategoryViewSet(GenericViewSet, ListModelMixin):
    permission_classes = (AllowAny,)
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['name', 'tags', 'handle']


class CustomerReturnViewSet(BaseModelViewSet):
    permission_classes = (IsAuthenticated, IsCustomer,)
    queryset = Return.objects.all()
    serializer_class = ReturnTrackingUpdateSerializer
    retrieve_serializer_class = ReturnModelSerializerGET

    @action(detail=False, methods=['POST'], url_path='add-return', serializer_class=ReturnModelSerializer)
    def create_record(self, request, *args, **kwargs):
        serializer = ReturnModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Successfully added return request.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)



