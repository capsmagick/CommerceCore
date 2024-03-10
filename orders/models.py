from django.db import models
from users.models.base_model import BaseModel
from users.models.other import AddressRegister
from product.models import Variant
from django.db.models import Sum



class Order(BaseModel):
    STATUS_CHOICES = (
        ('Order Placed', 'Order Placed'),
        ('Order Processing', 'Order Processing'),
        ('Packed', 'Packed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    order_id = models.CharField(max_length=20, verbose_name='Order Id')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Total Amount')
    currency = models.CharField(max_length=10,default='INR', null=True, blank=True, verbose_name='Currency')

    user = models.CharField(max_length=150, verbose_name='User')
    address = models.ForeignKey(AddressRegister, related_name='order_address', null=True, verbose_name='Address', on_delete=models.SET_NULL)

    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='Order Placed', verbose_name='Status')

    payment_id = models.CharField(max_length=256, null=True, blank=True, verbose_name='Payment ID')
    shipping_id = models.CharField(max_length=256, null=True, blank=True, verbose_name='Shipping ID')

    def calculate_total(self):
        total_amount = OrderItem.objects.first(order=self).aggregate(Sum('total_amount'))
        self.total_amount = total_amount['total_amount__sum']
        self.save()


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems', verbose_name='Order Details')
    product_variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='order_product',
                                        verbose_name='Order Variant')
    quantity = models.IntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Total Amount')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Price')

    def save(self, *args, **kwargs):
        total_amount = self.price * self.quantity
        self.total_amount = total_amount
        super().save(*args, **kwargs)
        self.order.calculate_total()

