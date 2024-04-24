import django_filters as filters
from django.db.models import Q

from product.models import Products
from product.models import Variant
from product.models import Collection
from product.models import LookBook
from masterdata.models import Category
from customer.models import Return
from customer.models import Review

from orders.models import Order


class CustomerProductFilter(filters.FilterSet):
    categories = filters.CharFilter(method='generate_categories_view')

    def generate_categories_view(self, queryset, value, *args, **kwargs):
        try:
            elements = args[0].split(',')
            categories_value = [int(num) for num in elements]
            if categories_value:
                queryset = queryset.filter(
                    Q(categories__in=categories_value) |
                    Q(categories__parent_category__in=categories_value)
                )
        except Exception as e:
            print('Exception occurred at the product section filter : ', str(e))
        return queryset

    class Meta:
        model = Products
        fields = ['categories']


class CustomerVariantFilter(filters.FilterSet):
    categories = filters.CharFilter(method='generate_categories_view')

    def generate_categories_view(self, queryset, value, *args, **kwargs):
        try:
            elements = args[0].split(',')
            categories_value = [int(num) for num in elements]
            if categories_value:
                queryset = queryset.filter(
                    Q(product__categories__in=categories_value) |
                    Q(product__categories__parent_category__in=categories_value)
                )
        except Exception as e:
            print('Exception occurred at the product section filter : ', str(e))
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
