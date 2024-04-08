import django_filters as filters

from .models import Category
from .models import Brand
from .models import AttributeGroup


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = ['parent_category', 'attribute_group', 'tags']


class BrandFilter(filters.FilterSet):
    class Meta:
        model = Brand
        fields = ['is_active', 'tags']


class AttributeGroupFilter(filters.FilterSet):
    class Meta:
        model = AttributeGroup
        fields = ['attributes']




