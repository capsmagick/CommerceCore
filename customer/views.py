from setup.views import BaseModelViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from setup.permissions import IsCustomer

from customer.models import Cart
from customer.models import CartItem
from customer.models import WishList

from customer.serializers import CartModelSerializer
from customer.serializers import CartItemModelSerializer
from customer.serializers import AddToCartSerializer
from customer.serializers import WishListModelSerializer
from customer.serializers import WishListGETSerializer



class CartModelViewSet(GenericViewSet):
    permission_classes = (IsCustomer,)
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

    @action(detail=False, methods=['DELETE'], url_path='(?P<id>.*?)/remove-cart')
    def delete_from_cart(self, request, pk, id):
        cart = self.get_user_cart(request)
        item = cart.cartitems.get(id=id)
        item.delete()
        return Response({
            'message': 'Successfully removed..!',
        }, status=status.HTTP_200_OK)


class WishListModelViewSet(GenericViewSet, ListModelMixin):
    permission_classes = (IsCustomer,)
    queryset = WishList.objects.all()
    serializer_class = WishListGETSerializer

    @action(detail=True, methods=['POST'], url_path='add-to-wishlist', serializer_class=WishListModelSerializer)
    def add_to_wishlist(self, request, pk):
        user = request.user
        serializer = WishListModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user)

        return Response({
            'data': serializer.data,
            'message': 'Successfully added to wishlist.!'
        })

    @action(detail=False, methods=['DELETE'], url_path='(?P<id>.*?)/remove-wishlist')
    def delete_from_cart(self, request, pk, id):
        user = request.user
        item = user.user_wishlist.get(id=id)
        item.delete()
        return Response({
            'message': 'Successfully removed..!',
        }, status=status.HTTP_200_OK)



