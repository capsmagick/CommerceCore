from django.core.management.base import BaseCommand

from customer.models import Cart
from product.models import Variant


class Command(BaseCommand):
    help = 'To restore the product, that are in the inactive cart'

    def handle(self, *args, **options):
        # TODO : Logic to get Inactive Cart
        inactive_cart = Cart.objects.all()

        for cart in inactive_cart:
            cart_items = cart.cartitems.all()

            for product in cart_items:
                Variant.objects.get(pk=product.product_variant_id).restore_stock(product.quantity)
                product.delete()


