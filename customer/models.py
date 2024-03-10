from django.db import models
from setup.models import BaseModel
from users.models import User
from product.models import Variant


class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_cart', verbose_name='User')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Total Amount')
    currency = models.CharField(default='INR', null=True, blank=True, verbose_name='Currency')


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems', verbose_name='Cart Details')
    product_variant = models.ForeignKey(Variant, on_delete=models.CASCADE, related_name='cart_product', verbose_name='Product Variant')
    quantity = models.IntegerField(default=1, verbose_name='Quantity')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Total Amount')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Price')
