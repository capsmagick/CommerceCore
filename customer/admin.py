from django.contrib import admin
from customer.models import Cart
from customer.models import CartItem
from customer.models import WishList


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_amount', 'currency')


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(WishList)
