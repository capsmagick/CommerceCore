from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from setup.views import BaseModelViewSet

from masterdata.models import Category
from masterdata.models import Brand
from masterdata.models import Tag
from masterdata.models import Attribute
from masterdata.models import AttributeGroup
from masterdata.models import Dimension
from masterdata.models import ReturnReason

from masterdata.serializers import CategoryModelSerializer
from masterdata.serializers import CategoryModelSerializerGET
from masterdata.serializers import BrandModelSerializer
from masterdata.serializers import BrandModelSerializerGET
from masterdata.serializers import TagModelSerializer
from masterdata.serializers import AttributeModelSerializer
from masterdata.serializers import RetrieveAttributeModelSerializer
from masterdata.serializers import AttributeGroupModelSerializer
from masterdata.serializers import RetrieveAttributeGroupModelSerializer
from masterdata.serializers import DimensionModelSerializer
from masterdata.serializers import RetrieveDimensionModelSerializer
from masterdata.serializers import ReturnReasonModelSerializer
from masterdata.serializers import ReturnReasonModelSerializerGET

from masterdata.filters import CategoryFilter
from masterdata.filters import BrandFilter
from masterdata.filters import AttributeGroupFilter


class CategoryModelViewSet(BaseModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    retrieve_serializer_class = CategoryModelSerializerGET
    search_fields = ['name', 'parent_category__name', 'description']
    default_fields = [
        'name', 'description', 'is_active', 'parent_category',
        'second_parent_category', 'attribute_group'
    ]
    filterset_class = CategoryFilter

    @action(detail=True, methods=['POST'], url_path='deactivate')
    def deactivate(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.deactivate()

        return Response({
            'message': f'{obj.name} successfully deactivated.!'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='activate')
    def activate(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.activate()

        return Response({
            'message': f'{obj.name} successfully activated.!'
        }, status=status.HTTP_200_OK)


class BrandModelViewSet(BaseModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandModelSerializer
    retrieve_serializer_class = BrandModelSerializerGET
    search_fields = ['name']
    default_fields = ['name', 'description']
    filterset_class = BrandFilter

    @action(detail=True, methods=['POST'], url_path='deactivate')
    def deactivate(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.deactivate()

        return Response({
            'message': f'{obj.name} successfully deactivated.!'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='activate')
    def activate(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.activate()

        return Response({
            'message': f'{obj.name} successfully activated.!'
        }, status=status.HTTP_200_OK)


class TagModelViewSet(BaseModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagModelSerializer
    search_fields = ['name']
    default_fields = ['name']


class AttributeModelViewSet(BaseModelViewSet):
    queryset = Attribute.objects.all()
    serializer_class = AttributeModelSerializer
    retrieve_serializer_class = RetrieveAttributeModelSerializer
    search_fields = ['name']
    default_fields = ['name', 'value']


class AttributeGroupModelViewSet(BaseModelViewSet):
    queryset = AttributeGroup.objects.all()
    serializer_class = AttributeGroupModelSerializer
    retrieve_serializer_class = RetrieveAttributeGroupModelSerializer
    search_fields = ['name']
    default_fields = ['name', 'attributes']
    filterset_class = AttributeGroupFilter


class DimensionModelViewSet(BaseModelViewSet):
    queryset = Dimension.objects.all()
    serializer_class = DimensionModelSerializer
    retrieve_serializer_class = RetrieveDimensionModelSerializer
    search_fields = ['length']
    default_fields = [
        'length', 'breadth', 'height',
        'dimension_unit', 'weight', 'weight_unit'
    ]


class ReturnReasonModelViewSet(BaseModelViewSet):
    queryset = ReturnReason.objects.all()
    serializer_class = ReturnReasonModelSerializer
    retrieve_serializer_class = ReturnReasonModelSerializerGET
    search_fields = ['title']
    default_fields = [
        'title', 'description',
    ]



