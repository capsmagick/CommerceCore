import django_filters as filters

from product.models import Variant
from product.models import Collection
from product.models import LookBook
from masterdata.models import Category
from customer.models import Return
from customer.models import Review


class CustomerVariantFilter(filters.FilterSet):
    class Meta:
        model = Variant
        fields = ['product']


class CustomerCollectionFilter(filters.FilterSet):
    class Meta:
        model = Collection
        fields = ['name', 'tags',]


class CustomerLookBookFilter(filters.FilterSet):
    class Meta:
        model = LookBook
        fields = ['variants']


class CustomerCategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = ['attribute_group', 'tags', 'handle', 'is_main_menu', 'is_top_category']


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
