import django_filters as filters

from product.models import Variant
from product.models import Collection
from product.models import LookBook
from masterdata.models import Category
from customer.models import Return


class CustomerVariantFilter(filters.FilterSet):
    class Meta:
        model = Variant
        fields = ['product', 'attributes']


class CustomerCollectionFilter(filters.FilterSet):
    class Meta:
        model = Collection
        fields = ['name', 'collections', 'tags']


class CustomerLookBookFilter(filters.FilterSet):
    class Meta:
        model = LookBook
        fields = ['variants']


class CustomerCategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = ['parent_category', 'second_parent_category', 'attribute_group', 'tags']


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
