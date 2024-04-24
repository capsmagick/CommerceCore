import django_filters as filters

from product.models import Products
from product.models import Variant
from product.models import ProductImage
from product.models import Collection
from product.models import CollectionItems
from product.models import LookBook
from product.models import LookBookItems


class ProductFilter(filters.FilterSet):
    categories = filters.CharFilter(method='generate_categories_view')

    def generate_categories_view(self, queryset, value, *args, **kwargs):
        try:
            elements = args[0].split(',')
            categories_value = [int(num) for num in elements]
            if categories_value:
                queryset = queryset.filter(categories__in=categories_value)
        except Exception as e:
            print('Exception occurred at the product section filter : ', str(e))
        return queryset

    class Meta:
        model = Products
        fields = ['condition', 'categories', 'brand', 'is_disabled']


class VariantFilter(filters.FilterSet):
    categories = filters.CharFilter(method='generate_categories_view')

    def generate_categories_view(self, queryset, value, *args, **kwargs):
        try:
            elements = args[0].split(',')
            categories_value = [int(num) for num in elements]
            if categories_value:
                queryset = queryset.filter(product__categories__in=categories_value)
        except Exception as e:
            print('Exception occurred at the variant section filter : ', str(e))
        return queryset

    class Meta:
        model = Variant
        fields = ['product', 'product__brand', 'categories']


class ProductImageFilter(filters.FilterSet):
    class Meta:
        model = ProductImage
        fields = ['product', 'variant']


class CollectionFilter(filters.FilterSet):
    class Meta:
        model = Collection
        fields = ['name']


class LookBookFilter(filters.FilterSet):
    class Meta:
        model = LookBook
        fields = ['name']


class CollectionItemsFilter(filters.FilterSet):
    class Meta:
        model = CollectionItems
        fields = ['collection', 'product']


class LookBookItemsFilter(filters.FilterSet):
    class Meta:
        model = LookBookItems
        fields = ['look_book', 'product']


