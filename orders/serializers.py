from rest_framework import serializers

from orders.models import Order
from orders.models import OrderItem


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

