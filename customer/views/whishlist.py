from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from setup.permissions import IsCustomer

from customer.models import WishList

from customer.serializers import WishListModelSerializer
from customer.serializers import WishListGETSerializer


class WishListModelViewSet(GenericViewSet, ListModelMixin):
    permission_classes = (IsAuthenticated, IsCustomer,)
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

