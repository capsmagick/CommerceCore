import django_filters as filters

from .models import Transaction


class TransactionFilter(filters.FilterSet):
    class Meta:
        model = Transaction
        fields = [
            'transaction_id',
            'status',
            'response_received_date',
            'order__user',
        ]

