from rest_framework import serializers

from customer.models import Cart
from customer.models import CartItem
from customer.models import WishList

from users.serializers import UserDataModelSerializer
from product.serializers import VariantModelSerializer


class CartModelSerializer(serializers.ModelSerializer):
    user = UserDataModelSerializer()
    created_by = UserDataModelSerializer()
    updated_by = UserDataModelSerializer()
    deleted_by = UserDataModelSerializer()
    items = serializers.SerializerMethodField()

    def get_items(self, attrs):
        items = attrs.cartitems.all()
        return CartItemModelSerializer(items, many=True).data

    class Meta:
        model = Cart
        fields = '__all__'


class CartItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = (
            'product_variant',
            'quantity',
            'price',
        )

    def create(self, validated_data):
        cart = validated_data.pop('cart')
        obj = CartItem.objects.create(cart=cart, **validated_data)
        return obj


class WishListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = (
            'product_variant',
        )

    def create(self, validated_data):
        user = validated_data.pop('user')
        obj = WishList.objects.create(user=user, **validated_data)
        return obj


class WishListGETSerializer(serializers.ModelSerializer):
    user = UserDataModelSerializer()
    product_variant = VariantModelSerializer()
    class Meta:
        model = WishList
        fields = '__all__'

