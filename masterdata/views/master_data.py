from setup.views import BaseModelViewSet

from masterdata.models import Category
from masterdata.models import Brand
from masterdata.models import Tag

from masterdata.serializers import CategoryModelSerializer
from masterdata.serializers import BrandModelSerializer
from masterdata.serializers import TagModelSerializer


class CategoryModelViewSet(BaseModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    search_fields = ['name', 'parent_category__name', 'description']
    default_fields = [
        'name', 'description', 'is_active', 'parent_category'
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



