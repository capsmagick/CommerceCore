from django.db import models
from users.models.base_model import BaseModel
from users.models.other import AddressRegister
from product.models import Variant
from customer.models import Cart
from django.db.models import Sum
import datetime
from django_fsm import FSMIntegerField
from django_fsm import transition


def generate_order_id():
    order_last = Order.objects.all().order_by('-id')
    if order_last.count() > 0:
        last_order_id = order_last[0].order_id
        number = int(last_order_id[6:]) + 1
    else:
        number = 1
    order_key = f"{number:06}"
    order_id = f"SC-ORD{order_key}"

    if Order.objects.filter(order_id=order_id).exists():
        return generate_order_id()
    return order_id


class Order(BaseModel):
    PENDING = 0
    PAYMENT_INITIATED = 1
    ORDER_PLACED = 2
    ORDER_PROCESSING = 3
    PACKED = 4
    READY_FOR_DISPATCH = 5
    SHIPPED = 6
    DELIVERED = 7
    CANCELLED = 14

    STATUS_CHOICES = (
        (PENDING, 'PENDING'),
        (PAYMENT_INITIATED, 'PAYMENT INITIATED'),
        (ORDER_PLACED, 'ORDER PLACED'),
        (ORDER_PROCESSING, 'ORDER PROCESSING'),
        (PACKED, 'PACKED'),
        (READY_FOR_DISPATCH, 'READY FOR DISPATCH'),
        (SHIPPED, 'SHIPPED'),
        (DELIVERED, 'DELIVERED'),
        (CANCELLED, 'CANCELLED'),
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

    status = FSMIntegerField(default=PENDING, choices=STATUS_CHOICES, verbose_name='Status', protected=True)

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

    @transition(field=status, source=[PENDING], target=PAYMENT_INITIATED)
    def order_payment(self):
        return f"{self.order_id} moved to Payment Initiated"

    @transition(field=status, source=[PAYMENT_INITIATED], target=PENDING)
    def order_pending(self):
        return f"{self.order_id} moved to Pending"

    @transition(field=status, source=[PAYMENT_INITIATED], target=ORDER_PLACED)
    def order_placed(self):
        return f"{self.order_id} moved to Order Placed"

    @transition(field=status, source=[ORDER_PLACED], target=ORDER_PROCESSING)
    def order_processing(self):
        return f"{self.order_id} moved to Order Processing"

    @transition(field=status, source=ORDER_PROCESSING, target=PACKED)
    def packing(self):
        return f"{self.order_id} moved Packed"

    @transition(field=status, source=[PACKED], target=READY_FOR_DISPATCH)
    def ready_for_dispatch(self):
        return f"{self.order_id} moved to Ready For Dispatch"

    @transition(field=status, source=[READY_FOR_DISPATCH], target=SHIPPED)
    def shipped(self):
        return f"{self.order_id} moved to Shipped"
    
    @transition(field=status, source=[SHIPPED], target=DELIVERED)
    def delivered(self):
        return f"{self.order_id} moved Delivered"

    # @transition(field=status, source=['Order Placed', 'Packed', 'Delivered'], target='Cancelled')
    # def cancelled(self):
    #     self.status = 'Cancelled'
    #     return f"{self.order_id} moved to Cancelled"


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

