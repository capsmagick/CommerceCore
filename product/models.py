from django.db import models

from masterdata.models import Category, Brand
from users.models.base_model import BaseModel
from masterdata.models import Tag, Attribute


class Products(BaseModel):
    name = models.CharField(max_length=50, verbose_name='Name')
    short_description = models.CharField(max_length=200, null=True, verbose_name='Short Description')
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    sku = models.CharField(max_length=50, blank=True, verbose_name='SKU')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Selling Price')
    # currency = models.CharField(max_length=3, default='INR',
    #                             verbose_name='Currency', null=True)  # [('USD', 'USD'), ('INR', 'INR')]
    condition = models.CharField(max_length=50, verbose_name='Condition')  # [('New', 'New'), ('Used', 'Used')]

    categories = models.ManyToManyField(Category,
                                        related_name='product_categories',
                                        verbose_name='Product Category')

    brand = models.ForeignKey(Brand, related_name='product_brand',
                              on_delete=models.CASCADE,
                              verbose_name='Brand')

    is_disabled = models.BooleanField(default=False, verbose_name='Disabled')
    hsn_code = models.CharField(max_length=20, blank=True, null=True, verbose_name='HSN Code')
    rating = models.IntegerField(verbose_name='Rating', blank=True, null=True)
    no_of_reviews = models.IntegerField(verbose_name='No. of Reviews', blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='tags', blank=True, null=True, verbose_name='Tags')

    # reviews = models.ManyToManyField('Review',
    #                                  related_name='product_reviews',
    #                                  verbose_name='Product Review')

    def __str__(self):
        return self.name


class Variant(BaseModel):
    product = models.ForeignKey(Products, related_name='product_variant',
                                on_delete=models.CASCADE,
                                verbose_name='Variant')
    attributes = models.ManyToManyField(Attribute, related_name='variant_attributes', blank=True, null=True,
                                        verbose_name='Attributes')

    def __str__(self):
        return f"{self.product.name}"


class ProductImage(BaseModel):
    product = models.ForeignKey(
        Products, related_name='product_images', verbose_name='Product Image',
        on_delete=models.SET_NULL, null=True, blank=True
    )

    variant = models.ForeignKey(
        Variant, related_name='variant_images', verbose_name='Variant Image',
        on_delete=models.SET_NULL, null=True, blank=True
    )

    image = models.FileField(upload_to='product_images/',
                             blank=True, null=True,
                             verbose_name='Image')
    thumbnail = models.ImageField(upload_to='product_images/thumbnail', blank=True, null=True,
                                  verbose_name='Thumbnail')
    alt_text = models.CharField(max_length=255, verbose_name='Alt Text')

    def __str__(self):
        return self.alt_text


class Collection(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Name')
    collections = models.ManyToManyField(Products,
                                         related_name='product_collections',
                                         verbose_name='Collections')

    def __str__(self):
        return self.name


class LookBook(BaseModel):
    name = models.CharField(max_length=100, verbose_name='Name')

    variants = models.ManyToManyField(Variant,
                                      related_name='variants',
                                      verbose_name='Variants')
