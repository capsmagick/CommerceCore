from setup.views import BaseModelViewSet

from masterdata.models import Category
from masterdata.models import Brand
from masterdata.models import Tag
from masterdata.models import Attribute
from masterdata.models import AttributeGroup
from masterdata.models import Dimension

from masterdata.serializers import CategoryModelSerializer
from masterdata.serializers import BrandModelSerializer
from masterdata.serializers import TagModelSerializer
from masterdata.serializers import AttributeModelSerializer
from masterdata.serializers import RetrieveAttributeModelSerializer
from masterdata.serializers import AttributeGroupModelSerializer
from masterdata.serializers import RetrieveAttributeGroupModelSerializer
from masterdata.serializers import DimensionModelSerializer
from masterdata.serializers import RetrieveDimensionModelSerializer


class CategoryModelViewSet(BaseModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    search_fields = ['name', 'parent_category__name', 'description']
    default_fields = [
        'name', 'description', 'is_active', 'parent_category',
        'second_parent_category', 'attribute_group'
    ]


class BrandModelViewSet(BaseModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandModelSerializer
    search_fields = ['name']
    default_fields = ['name', 'description']


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


class DimensionModelViewSet(BaseModelViewSet):
    queryset = Dimension.objects.all()
    serializer_class = DimensionModelSerializer
    retrieve_serializer_class = RetrieveDimensionModelSerializer
    search_fields = ['name']
    default_fields = [
        'length', 'breadth', 'height',
        'dimension_unit', 'weight', 'weight_unit'
    ]



