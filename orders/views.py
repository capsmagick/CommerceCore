from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from setup.views import BaseModelViewSet
from setup.permissions import IsCustomer

from orders.models import Order
from orders.models import OrderItem
from customer.models import Cart

from orders.serializers import OrderModelSerializer
from orders.serializers import PlaceOrderSerializer
from orders.serializers import BuyNowSerializer
from orders.serializers import OrderItemModelSerializer


class PlaceOrder(GenericViewSet):
    permission_classes = (IsAuthenticated, IsCustomer,)
    queryset = Order.objects.all()

    def get_user_cart(self, request):
        cart, created = Cart.objects.get(
            user_id=request.user.id, deleted=False
        )
        return cart

    @action(detail=False, methods=['POST'], url_path='place-order', serializer_class=PlaceOrderSerializer)
    def place_order(self, request):
        serializer = PlaceOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = self.get_user_cart(request)

        new_order = Order.objects.create(
            total_amount=cart.total_amount,
            user=cart.user.username,
            address=serializer.validated_data.get('address'),
            status='Order Placed'
        )

        cart_items = cart.cartitems.filter(deleted=False)

        order_items = []
        for item in cart_items:
            order_items.append(
                OrderItem(
                    order=new_order, product_variant=item.product_variant,
                    quantity=item.quantity, total_amount=item.total_amount,
                    price=item.price
                )
            )

        OrderItem.objects.bulk_create(order_items)

        return Response({
            'message': 'Successfully created new order..!'
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], url_path='buy-now', serializer_class=BuyNowSerializer)
    def place_order(self, request):
        user = request.user
        serializer = BuyNowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_order = Order.objects.create(
            user=user.username,
            address_id=serializer.validated_data.get('address'),
            status='Order Placed'
        )

        variant = serializer.validated_data.get('product_variant')

        product = variant.get('id')
        price = product.get('price')

        OrderItem.objects.create(
            order=new_order, product_variant=product.get('id'),
            quantity=1, price=price, total_amount=price
        )

        return Response({
            'message': 'Successfully created new order..!'
        }, status=status.HTTP_200_OK)


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

