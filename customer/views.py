from setup.views import BaseModelViewSet

from customer.models import Cart
from customer.models import CartItem

from customer.serializers import CartModelSerializer
from customer.serializers import CartItemModelSerializer


class CartModelViewSet(BaseModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartModelSerializer
    default_fields = [
        'user',
        'total_amount',
        'currency'
    ]


class CartItemModelViewSet(BaseModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemModelSerializer
    default_fields = [
        'cart',
        'product_variant',
        'quantity',
        'total_amount',
        'price'
    ]
