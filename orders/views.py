from setup.views import BaseModelViewSet

from orders.models import Order
from orders.models import OrderItem

from orders.serializers import OrderModelSerializer
from orders.serializers import OrderItemModelSerializer


class OrderModelViewSet(BaseModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderModelSerializer
    default_fields = [
        'order_id', 'total_amount', 'user', 'address',
        'status', 'payment_id', 'shipping_id'
    ]


class OrderItemModelViewSet(BaseModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemModelSerializer
    default_fields = [
        'order', 'product_variant', 'quantity', 'price',
    ]

