from rest_framework import serializers

from customer.models import Cart

from customer.models import CartItem


class CartModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'
