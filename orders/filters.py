import django_filters as filters
from orders.models import Order


class OrderFiler(filters.FilterSet):

    class Meta:
        model = Order
        fields = [
            'status',
            'user',
        ]

