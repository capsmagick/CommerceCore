from django.db import models
from django.db.models import Sum
from django_fsm import transition

import datetime

from users.models.base_model import BaseModel
from users.models import User
from product.models import Variant
from product.models import Products
from masterdata.models import ReturnReason


def generate_order_id():
    now = datetime.datetime.now()
    order_key = "".join(now.strftime("%Y%b%d%H%M%S%f"))
    return f"RET{order_key}"


class WishList(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_wishlist', verbose_name='User', null=True
    )
    product_variant = models.ForeignKey(
        Variant, on_delete=models.CASCADE, related_name='wishlist_product', verbose_name='Product'
    )


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_cart', verbose_name='User', null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Total Amount')
    currency = models.CharField(max_length=10, default='INR', null=True, blank=True, verbose_name='Currency')

    def calculate_total(self):
        total_amount = CartItem.objects.first(order=self, deleted=False).aggregate(Sum('total_amount'))
        self.total_amount = total_amount['total_amount__sum']
        self.save()


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems', verbose_name='Cart Details')
    product_variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='cart_product', verbose_name='Product Variant')
    quantity = models.IntegerField(default=1, verbose_name='Quantity')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Total Amount')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Price')

    def save(self, *args, **kwargs):
        total_amount = self.price * self.quantity
        self.total_amount = total_amount
        super().save(*args, **kwargs)
        self.cart.calculate_total()


    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.product_variant.restore_stock(self.quantity)


class Review(BaseModel):
    RATING_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )

    product = models.ForeignKey(
        Products, on_delete=models.SET_NULL,
        related_name='product_review', null=True,
        verbose_name="Product"
    )

    comment = models.TextField(null=True, verbose_name='Comment')

    rating = models.CharField(max_length=5, default='0', null=True, verbose_name='Rating', choices=RATING_CHOICES)


class ReviewImage(BaseModel):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='review_image',
        verbose_name='Review', null=True
    )

    file = models.FileField(upload_to='review/image', verbose_name='Image', blank=True, null=True)


class Return(BaseModel):
    STATUS_CHOICES = (
        ('Submitted', 'Submitted'),
        ('In Review', 'In Review'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    REFUND_METHOD = (
        ('Exchange', 'Exchange'),
        ('Refund', 'Refund'),
    )

    REFUND_CHOICES = (
        ('Pending', 'Pending'),
        ('In Transit', 'In Transit'),
        ('Delivered', 'Delivered'),
        ('Refund Initiated', 'Refund Initiated'),
        ('Refunded', 'Refunded'),
    )

    return_id = models.CharField(max_length=100, verbose_name='Return Id', null=True, blank=True)

    reason = models.ForeignKey(
        ReturnReason, on_delete=models.SET_NULL, related_name='return_season',
        verbose_name='Reason', null=True
    )

    product = models.ForeignKey(
        Variant, on_delete=models.SET_NULL, related_name='return_product',
        verbose_name='Product', null=True
    )

    purchase_bill = models.FileField(upload_to='return/bill', null=True, blank=True, verbose_name='Purchase Bill')
    description = models.TextField(blank=True, null=True, verbose_name='Description')

    refund_method = models.CharField(
        choices=REFUND_METHOD, max_length=70, blank=True, null=True, verbose_name='Refund Method'
    )

    tracking_id = models.CharField(max_length=256, blank=True, null=True, verbose_name='Tracking ID')
    shipping_agent = models.CharField(max_length=256, blank=True, null=True, verbose_name='Shipping Agent')


    status = models.CharField(
        choices=STATUS_CHOICES, max_length=25, default='Submitted', verbose_name='Status'
    )

    approved_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='approved_user',
        blank=True, null=True, verbose_name='Approved User'
    )
    approved_comment = models.TextField(blank=True, null=True, verbose_name='Approved Comment')
    approved_at = models.DateTimeField(blank=True, null=True, verbose_name='Approved Date')

    rejected_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='rejected_user',
        blank=True, null=True, verbose_name='Approved User'
    )
    rejected_comment = models.TextField(blank=True, null=True, verbose_name='Rejected Comment')
    rejected_at = models.DateTimeField(blank=True, null=True, verbose_name='Rejected Date')

    # Refund
    refund_status = models.CharField(
        choices=REFUND_CHOICES, max_length=25, blank=True, null=True, verbose_name='Refund Status'
    )
    refund_tracking_id = models.CharField(max_length=256, blank=True, null=True, verbose_name='Refund Tracking ID')
    refund_shipping_agent = models.CharField(max_length=256, blank=True, null=True, verbose_name='Refund Shipping Agent')
    refund_transaction_id = models.CharField(max_length=256, blank=True, null=True, verbose_name='Refund Tracking ID')

    def save(self, *args, **kwargs):
        if not self.return_id:
            self.return_id = generate_order_id()
        super().save(*args, **kwargs)

    @transition(field=status, source=['Submitted'], target='In Review')
    def in_review(self):
        return f"{self.return_id} moved to In Review"

    @transition(field=status, source=['In Review'], target='Approved')
    def approve(self):
        return f"{self.return_id} moved Approved"

    @transition(field=status, source=['In Review'], target='Rejected')
    def reject(self):
        return f"{self.return_id} moved to Reject"

    @transition(field=refund_status, source=['Pending'], target='In Transit')
    def in_transit(self):
        return f"{self.return_id} moved to In Transit"

    @transition(field=refund_status, source=['In Transit'], target='Delivered')
    def delivered(self):
        return f"{self.return_id} moved Delivered"

    @transition(field=refund_status, source=['Pending'], target='Refund Initiated')
    def refund_initiated(self):
        return f"{self.return_id} moved to Refund Initiated"

    @transition(field=refund_status, source=['Refund Initiated'], target='Refunded')
    def refunded(self):
        return f"{self.return_id} moved to Refunded"



