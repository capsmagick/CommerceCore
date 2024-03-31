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
    class Meta:
        model = Transaction
        fields = '__all__'


