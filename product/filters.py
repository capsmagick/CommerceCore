import django_filters as filters

from product.models import Products
from product.models import Variant
from product.models import ProductImage
from product.models import Collection
from product.models import LookBook


class ProductFilter(filters.Filter):
    class Meta:
        model = Products
        fields = ['condition', 'categories', 'brand', 'is_disabled', 'tags']


class VariantFilter(filters.Filter):
    class Meta:
        model = Variant
        fields = ['product', 'attributes', 'product__brand', 'product__categories', 'product__tags']


class ProductImageFilter(filters.Filter):
    class Meta:
        model = ProductImage
        fields = ['product', 'variant']


class CollectionFilter(filters.Filter):
    class Meta:
        model = Collection
        fields = ['collections']


class LookBookFilter(filters.Filter):
    class Meta:
        model = LookBook
        fields = ['variants']


