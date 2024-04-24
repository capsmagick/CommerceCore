from django.db import models
from users.models.base_model import BaseModel
from orders.models import Order


def generate_transaction_id():
    user_txn = Transaction.objects.all().order_by('-id')
    if user_txn.count() > 0:
        last_txn_id = user_txn[0].transaction_id
        number = int(last_txn_id[6:]) + 1
    else:
        number = 1

    txn_key = f"{number:06}"
    txn_id = f"SC-TXN{txn_key}"

    if Transaction.objects.filter(transaction_id=txn_id).exists():
        return generate_transaction_id()
    return txn_id


class Transaction(BaseModel):
    transaction_id = models.CharField(max_length=200, null=True, verbose_name='Transaction ID')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Amount')

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Order')

    status = models.CharField(max_length=25, blank=True, null=True)

    response = models.TextField(default='No Response')
    error = models.TextField(blank=True, null=True)

    response_received_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_id}"

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            transaction_id = generate_transaction_id()
            self.transaction_id = transaction_id
        super().save(*args, **kwargs)

    @classmethod
    def create_transaction(cls, order):
        return cls.objects.create(
            order=order,
            amount=order.total_amount,
            status='Initiated'
        )


