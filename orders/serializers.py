from rest_framework import serializers

from orders.models import Order
from orders.models import OrderItem
from users.models import AddressRegister
from product.serializers import VariantModelSerializerGET


class OrderModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'user',
            'address'
        )


class OrderItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'order',
            'product_variant',
            'quantity',
            'price',
        )


class PlaceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'address',
        )


class BuyNowSerializer(serializers.Serializer):
    product_variant = VariantModelSerializerGET()
    address = serializers.SlugRelatedField(slug_field='id', queryset=AddressRegister.objects.all())


