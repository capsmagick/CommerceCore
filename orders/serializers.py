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


class OrderItemRetrieveModelSerializer(serializers.ModelSerializer):
    product_variant = VariantModelSerializerGET()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    class Meta:
        model = OrderItem
        fields = '__all__'


class PlaceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'address',
        )


class BuyNowSerializer(serializers.Serializer):
    product_variant = VariantModelSerializerGET()
    address = serializers.SlugRelatedField(slug_field='id', queryset=AddressRegister.objects.all())


class OrderRetrieveSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    orderitems = OrderItemRetrieveModelSerializer(many=True, read_only=True)
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    class Meta:
        model = Order
        fields = '__all__'


class OrderItemsModelSerializerGET(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    class Meta:
        model = Order
        fields = '__all__'


