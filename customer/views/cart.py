from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from setup.permissions import IsCustomer

from customer.models import Cart
from product.models import Variant

from customer.serializers.serializers import CartModelSerializer
from customer.serializers.serializers import UpdateCartProductSerializer
from customer.serializers.serializers import AddToCartSerializer


class CartModelViewSet(GenericViewSet):
    permission_classes = (IsAuthenticated, IsCustomer,)
    queryset = Cart.objects.all()
    serializer_class = CartModelSerializer
    default_fields = [
        'user',
        'total_amount',
        'currency'
    ]

    def get_user_cart(self, request):
        cart, created = Cart.objects.get_or_create(
            user_id=request.user.id, deleted=False
        )
        return cart

    @action(detail=False, methods=['GET'], url_path='user-cart')
    def get_cart(self, request):
        cart = self.get_user_cart(request)
        return Response(CartModelSerializer(cart).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'], url_path='add-to-cart', serializer_class=AddToCartSerializer)
    def add_to_cart(self, request, pk):
        cart = self.get_user_cart(request)
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(cart)

        return Response({
            'data': serializer.data,
            'message': 'Successfully added to the cart.!'
        })

    @action(detail=False, methods=['POST'], url_path='update-cart-product', serializer_class=UpdateCartProductSerializer)
    def update_cart_product(self, request, pk):
        cart = self.get_user_cart(request)
        serializer = UpdateCartProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_variant = serializer.validated_data.get('product_variant')
        quantity = serializer.validated_data.get('quantity')

        cart_item = cart.cartitems.get(
            cart=cart, product_variant=product_variant
        )
        cart_item.quantity += quantity
        cart_item.save()
        Variant.objects.get(pk=product_variant).update_stock(quantity)

        return Response({
            'data': serializer.data,
            'message': 'Successfully added to the cart.!'
        })

    @action(detail=False, methods=['DELETE'], url_path='(?P<id>.*?)/remove-cart')
    def delete_from_cart(self, request, pk, id):
        cart = self.get_user_cart(request)
        item = cart.cartitems.get(id=id)
        item.delete()
        return Response({
            'message': 'Successfully removed..!',
        }, status=status.HTTP_200_OK)



