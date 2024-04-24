from django.db import models

from product.models import Variant
from users.models.base_model import BaseModel


class Tax(BaseModel):
    name = models.CharField(max_length=25, blank=True, null=True, verbose_name='Name')
    slab = models.CharField(max_length=25, blank=True, null=True, verbose_name='Slab')

    def __str__(self):
        return self.name


class Warehouse(BaseModel):
    name = models.CharField(max_length=30, blank=True, null=True, verbose_name='Name')

    def __str__(self):
        return self.name


class Batch(BaseModel):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Warehouse')
    batch_number = models.CharField(max_length=25, blank=True, null=True, verbose_name='Batch Number')
    rack = models.CharField(max_length=25, blank=True, null=True, verbose_name='Rack')
    row = models.CharField(max_length=25, blank=True, null=True, verbose_name='Row')
    expiry_date = models.DateField(blank=True, null=True, verbose_name='Expiry Date')
    purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Purchase Amount')
    mrp = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='MRP')
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Selling Price')
    purchase_quantity = models.IntegerField(default=0, verbose_name='Purchase Quantity')
    stock = models.IntegerField(default=0, verbose_name='stock')
    is_perishable = models.BooleanField(default=False, verbose_name='Perishable')
    is_disabled = models.BooleanField(default=False, verbose_name='Disabled')
    tax_inclusive = models.BooleanField(default=True, verbose_name='Tax Inclusive')
    purchase_amount_tax_inclusive = models.BooleanField(default=True, verbose_name='Purchase Amount Tax Inclusive')
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, related_name='tax', verbose_name='Tax', null=True, blank=True)

    def __str__(self):
        return self.batch_number


class Inventory(BaseModel):
    variants = models.ManyToManyField(Variant,
                                      related_name='inventoryvariants',
                                      verbose_name='Variants')

    stock = models.IntegerField(default=0, verbose_name='stock')

    batch = models.ManyToManyField(Batch,
                                   related_name='variants',
                                   verbose_name='Variants')

    low_stock_notification = models.IntegerField(default=0, verbose_name='stock')
