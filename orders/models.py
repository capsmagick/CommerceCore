from django.db import models
from users.models.base_model import BaseModel
from users.models.other import AddressRegister
from product.models import Variant
from customer.models import Cart
from django.db.models import Sum
import datetime
from django_fsm import transition


def generate_order_id():
    now = datetime.datetime.now()
    order_key = "".join(now.strftime("%Y%b%d%H%M%S%f"))
    order_id = f"ORD{order_key}"

    if Order.objects.filter(order_id=order_id).exists():
        return generate_order_id()
    return order_id



class Order(BaseModel):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Payment Initiated', 'Payment Initiated'),
        ('Order Placed', 'Order Placed'),
        ('Order Processing', 'Order Processing'),
        ('Packed', 'Packed'),
        ('Ready For Dispatch', 'Ready For Dispatch'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    cart = models.ForeignKey(
        Cart, related_name='cart_order', null=True, blank=True,
        verbose_name='Cart', on_delete=models.SET_NULL
    )

    order_id = models.CharField(max_length=70, verbose_name='Order Id')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Total Amount')
    currency = models.CharField(max_length=10,default='INR', null=True, blank=True, verbose_name='Currency')

    user = models.CharField(max_length=150, verbose_name='User')
    address = models.ForeignKey(AddressRegister, related_name='order_address', null=True, verbose_name='Address', on_delete=models.SET_NULL)

    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default='Pending', verbose_name='Status')

    payment_id = models.CharField(max_length=256, null=True, blank=True, verbose_name='Payment ID')
    shipping_id = models.CharField(max_length=256, null=True, blank=True, verbose_name='Shipping ID')

    def calculate_total(self):
        total_amount = OrderItem.objects.filter(order=self).aggregate(Sum('total_amount'))
        self.total_amount = total_amount['total_amount__sum'] if total_amount['total_amount__sum'] else 0.00
        self.save()

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = generate_order_id()
        super().save(*args, **kwargs)

    # @transition(field=status, source=['Pending'], target='Payment Initiated')
    def order_payment(self):
        self.status = 'Payment Initiated'
        return f"{self.order_id} moved to Payment Initiated"

    # @transition(field=status, source=['Payment Initiated'], target='Pending')
    def order_pending(self):
        self.status = 'Pending'
        return f"{self.order_id} moved to Pending"

    # @transition(field=status, source=['Payment Initiated'], target='Order Placed')
    def order_placed(self):
        self.status = 'Order Placed'
        return f"{self.order_id} moved to Order Placed"

    # @transition(field=status, source=['Order Placed'], target='Order Processing')
    def order_processing(self):
        self.status = 'Order Processing'
        return f"{self.order_id} moved to Order Processing"

    # @transition(field=status, source=['Order Processing'], target='Packed')
    def packing(self):
        self.status = 'Packed'
        return f"{self.order_id} moved Packed"

    # @transition(field=status, source=['Packed'], target='Ready For Dispatch')
    def ready_for_dispatch(self):
        self.status = 'Ready For Dispatch'
        return f"{self.order_id} moved to Ready For Dispatch"

    # @transition(field=status, source=['Ready For Dispatch'], target='Shipped')
    def shipped(self):
        self.status = 'Shipped'
        return f"{self.order_id} moved to Shipped"
    
    # @transition(field=status, source=['Shipped'], target='Delivered')
    def delivered(self):
        self.status = 'Delivered'
        return f"{self.order_id} moved Delivered"

    # @transition(field=status, source=['Order Placed', 'Packed', 'Delivered'], target='Cancelled')
    def cancelled(self):
        self.status = 'Cancelled'
        return f"{self.order_id} moved to Cancelled"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems', verbose_name='Order Details')
    product_variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='order_product',
                                        verbose_name='Order Variant')
    quantity = models.IntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Total Amount')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Price')

    def save(self, *args, **kwargs):
        if not self.total_amount:
            total_amount = self.price * self.quantity
            self.total_amount = total_amount
        super().save(*args, **kwargs)
        self.order.calculate_total()

