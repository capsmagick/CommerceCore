import django_filters as filters

from masterdata.models import Category
from masterdata.models import Brand
from masterdata.models import AttributeGroup


class CategoryFilter(filters.Filter):
    class Meta:
        model = Category
        fields = ['parent_category', 'second_parent_category', 'attribute_group', 'tags']


class BrandFilter(filters.Filter):
    class Meta:
        model = Brand
        fields = ['is_active', 'tags']


class AttributeGroupFilter(filters.Filter):
    class Meta:
        model = AttributeGroup
        fields = ['attributes']




