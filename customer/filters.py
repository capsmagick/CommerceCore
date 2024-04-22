import json

import django_filters as filters

from product.models import Products
from product.models import Variant
from product.models import Collection
from product.models import LookBook
from masterdata.models import Category
from customer.models import Return
from customer.models import Review

from orders.models import Order


class CustomerProductFilter(filters.FilterSet):
    categories = filters.CharFilter(method='generate_view')

    def generate_view(self, queryset, value, *args, **kwargs):
        try:
            categories = json.loads(args[0])
            if categories:
                queryset = queryset.filter(categories__in=categories)
        except Exception as e:
            print('Exception occurred at the hero section filter : ', str(e))
        return queryset

    class Meta:
        model = Products
        fields = ['categories']


class CustomerVariantFilter(filters.FilterSet):
    categories = filters.CharFilter(method='generate_view')

    def generate_view(self, queryset, value, *args, **kwargs):
        try:
            categories = json.loads(args[0])
            if categories:
                queryset = queryset.filter(product__categories__in=categories)
        except Exception as e:
            print('Exception occurred at the hero section filter : ', str(e))
        return queryset

    class Meta:
        model = Variant
        fields = ['product', 'categories']


class CustomerCollectionFilter(filters.FilterSet):
    class Meta:
        model = Collection
        fields = ['name']


class CustomerLookBookFilter(filters.FilterSet):
    class Meta:
        model = LookBook
        fields = ['name']


class CustomerCategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = ['attribute_group', 'handle', 'is_main_menu', 'is_top_category']


class CustomerReturnFilter(filters.FilterSet):
    class Meta:
        model = Return
        fields = [
            'reason',
            'product',
            'refund_method',
            'shipping_agent',
            'status',
            'approved_user',
            'rejected_user',
            'refund_status'
        ]


class CustomerReviewFilter(filters.FilterSet):
    class Meta:
        model = Review
        fields = [
            'product__name',
            'rating',
        ]


class CustomerOrderFilter(filters.FilterSet):
    class Meta:
        model = Order
        fields = ['order_id']
