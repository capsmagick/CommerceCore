from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from setup.views import BaseModelViewSet
from setup.export import ExportData

from .models import Category
from .models import Brand
from .models import Attribute
from .models import AttributeGroup
from .models import Dimension
from .models import ReturnReason

from .serializers import CategoryModelSerializer
from .serializers import CategoryModelSerializerGET
from .serializers import BrandModelSerializer
from .serializers import BrandModelSerializerGET
from .serializers import AttributeModelSerializer
from .serializers import RetrieveAttributeModelSerializer
from .serializers import AttributeGroupModelSerializer
from .serializers import RetrieveAttributeGroupModelSerializer
from .serializers import DimensionModelSerializer
from .serializers import RetrieveDimensionModelSerializer
from .serializers import ReturnReasonModelSerializer
from .serializers import ReturnReasonModelSerializerGET

from .filters import CategoryFilter
from .filters import BrandFilter
from .filters import AttributeGroupFilter


class CategoryModelViewSet(BaseModelViewSet, ExportData):
    queryset = Category.objects.all().order_by('id')
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


class BrandModelViewSet(BaseModelViewSet, ExportData):
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


class AttributeModelViewSet(BaseModelViewSet, ExportData):
    queryset = Attribute.objects.all()
    serializer_class = AttributeModelSerializer
    retrieve_serializer_class = RetrieveAttributeModelSerializer
    search_fields = ['name']
    default_fields = ['name', 'value']


class AttributeGroupModelViewSet(BaseModelViewSet, ExportData):
    queryset = AttributeGroup.objects.all()
    serializer_class = AttributeGroupModelSerializer
    retrieve_serializer_class = RetrieveAttributeGroupModelSerializer
    search_fields = ['name']
    default_fields = ['name', 'attributes']
    filterset_class = AttributeGroupFilter


class DimensionModelViewSet(BaseModelViewSet, ExportData):
    queryset = Dimension.objects.all()
    serializer_class = DimensionModelSerializer
    retrieve_serializer_class = RetrieveDimensionModelSerializer
    search_fields = ['length']
    default_fields = [
        'length', 'breadth', 'height',
        'dimension_unit', 'weight', 'weight_unit'
    ]


class ReturnReasonModelViewSet(BaseModelViewSet, ExportData):
    queryset = ReturnReason.objects.all()
    serializer_class = ReturnReasonModelSerializer
    retrieve_serializer_class = ReturnReasonModelSerializerGET
    search_fields = ['title']
    default_fields = [
        'title', 'description',
    ]



