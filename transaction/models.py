from django.db import models
from users.models.base_model import BaseModel
from orders.models import Order


class Transaction(BaseModel):
    transaction_id = models.CharField(max_length=200, null=True, verbose_name='Transaction ID')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Amount')

    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, verbose_name='Order')

    status = models.CharField(max_length=25, blank=True, null=True)

    response = models.TextField(default='No Response')
    error = models.TextField(blank=True, null=True)

    response_received_date = models.DateTimeField(blank=True, null=True)


