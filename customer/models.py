from django.db import models
from users.models.base_model import BaseModel
from users.models import User
from product.models import Variant
from django.db.models import Sum


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
    currency = models.CharField(max_length=10,default='INR', null=True, blank=True, verbose_name='Currency')

    def calculate_total(self):
        total_amount = CartItem.objects.first(order=self).aggregate(Sum('total_amount'))
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
