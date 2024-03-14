from django.contrib import admin

from product.models import Products
from product.models import Variant
from product.models import Collection
from product.models import LookBook
from product.models import ProductImage


admin.site.register(Products)
admin.site.register(Variant)
admin.site.register(Collection)
admin.site.register(LookBook)
admin.site.register(ProductImage)

