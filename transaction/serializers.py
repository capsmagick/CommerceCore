from rest_framework import serializers

from orders.serializers import OrderRetrieveSerializer
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'order',
        )


class TransactionRetrieveSerializer(serializers.ModelSerializer):
    order = OrderRetrieveSerializer()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    class Meta:
        model = Transaction
        fields = '__all__'


