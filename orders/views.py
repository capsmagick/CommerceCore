from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin

from django.db.models import Q
from django.shortcuts import get_object_or_404

from setup.permissions import IsCustomer
from setup.permissions import IsSuperUser
from setup.utils import generate_column

from transaction.views import ShipRocketUtility

from customer.models import Cart

from .models import Order
from .models import OrderItem

from .serializers import PlaceOrderSerializer
from .serializers import BuyNowSerializer
from .serializers import OrderRetrieveSerializer


class PlaceOrder(GenericViewSet, RetrieveModelMixin):
    permission_classes = (IsAuthenticated, IsCustomer,)
    queryset = Order.objects.all()
    serializer_class = OrderRetrieveSerializer

    def get_object(self):
        queryset = self.get_queryset()
        or_condition = Q()
        try:
            instance = int(self.kwargs['pk'])
            or_condition.add(
                Q(pk=instance), Q.OR
            )
        except ValueError:
            or_condition.add(
                Q(order_id=self.kwargs['pk']), Q.OR
            )
        obj = get_object_or_404(queryset, or_condition)
        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=False, methods=['POST'], url_path='place-order', serializer_class=PlaceOrderSerializer)
    def place_order(self, request):
        """
            API For Place Order

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
            Data:
                all data in the PlaceOrderSerializer serializer

            Returns:
                Response: A DRF Response object indicating success or failure and a message with order details.
        """

        serializer = PlaceOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = Cart.get_user_cart()

        new_order = Order.objects.create(
            cart=cart,
            total_amount=cart.total_amount,
            user=cart.user.username,
            address=serializer.validated_data.get('address'),
            status=Order.PENDING
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
            'message': 'Successfully created new order..!',
            'data': OrderRetrieveSerializer(new_order).data
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], url_path='buy-now', serializer_class=BuyNowSerializer)
    def buy_now(self, request):
        """
            API For Instant Buy

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
            Data:
                all data in the BuyNowSerializer serializer

            Returns:
                Response: A DRF Response object indicating success or failure and a message with order details.
        """

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


class OrderModelViewSet(GenericViewSet, ListModelMixin):
    """
        API for Order details for Admin user
    """

    permission_classes = (IsAuthenticated, IsSuperUser,)
    queryset = Order.objects.all()
    serializer_class = OrderRetrieveSerializer
    default_fields = [
        'order_id', 'total_amount', 'user', 'address',
        'status', 'payment_id', 'shipping_id'
    ]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        try:
            response.data['columns'] = generate_column(
                self.queryset.model, actions=True,
                default_fields=self.default_fields
            )
        except Exception as e:
            print('Exception occurred while generating the columns : ', e)
        return response

    @action(detail=True, methods=['POST'], url_path='order-processing')
    def order_processing(self, request, pk, *args, **kwargs):
        """
            API For Updating the order pending to order processing.

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
                pk (int): Primary key of the order model

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """

        obj = self.get_object()

        message = obj.order_processing()
        obj.save()

        return Response({
            'message': message,
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='packing')
    def packing(self, request, pk, *args, **kwargs):
        """
            API For Updating the order processing to order packing.

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
                pk (int): Primary key of the order model

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """
        obj = self.get_object()

        message = obj.packing()
        obj.save()

        return Response({
            'message': message,
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='ready-for-dispatch')
    def ready_for_dispatch(self, request, pk, *args, **kwargs):
        """
            API For updating the order packed to ready for dispatch.
            Also creating order in shiprocket and requesting shipment
        """
        obj = self.get_object()

        message = obj.ready_for_dispatch()

        """Creating order in shiprocket"""
        ShipRocketUtility().create_order(obj)

        obj.save()

        return Response({
            'message': message,
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='shipped')
    def shipped(self, request, pk, *args, **kwargs):
        """
            API For Updating the order packing to order shipped.

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
                pk (int): Primary key of the order model

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """
        obj = self.get_object()

        message = obj.shipped()
        obj.save()

        return Response({
            'message': message,
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='delivered')
    def delivered(self, request, *args, **kwargs):
        """
            API For Updating the order shipped to order delivered.

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
                pk (int): Primary key of the order model

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """
        obj = self.get_object()

        message = obj.delivered()
        obj.save()

        return Response({
            'message': message,
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='cancel')
    def cancelled(self, request, *args, **kwargs):
        pass


