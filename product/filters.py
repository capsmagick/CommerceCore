import django_filters as filters

from product.models import Products
from product.models import Variant
from product.models import ProductImage
from product.models import Collection
from product.models import LookBook


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Products
        fields = ['condition', 'categories', 'brand', 'is_disabled', 'tags']


class VariantFilter(filters.FilterSet):
    class Meta:
        model = Variant
        fields = ['product', 'product__brand', 'product__categories', 'product__tags']


class ProductImageFilter(filters.FilterSet):
    class Meta:
        model = ProductImage
        fields = ['product', 'variant']


class CollectionFilter(filters.FilterSet):
    class Meta:
        model = Collection
        fields = ['collections']


class LookBookFilter(filters.FilterSet):
    class Meta:
        model = LookBook
        fields = ['variants']


