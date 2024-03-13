from django.db import models
from users.models.base_model import BaseModel
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField

User = get_user_model()


class Brand(BaseModel):
    name = models.CharField(max_length=75, blank=True, null=True, verbose_name='Name', db_index=True)
    logo = models.FileField(upload_to='brand/logo', blank=True, null=True, verbose_name='Logo')
    description = models.TextField(blank=True, null=True, verbose_name='Description')

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField(max_length=75, blank=True, null=True, verbose_name='Name', db_index=True)

    def __str__(self):
        return self.name


class Attribute(BaseModel):
    name = models.CharField(max_length=80, null=True, verbose_name='Name')
    value = ArrayField(models.CharField(max_length=100), blank=True, null=True, default=list, verbose_name='Values')
    # value = models.JSONField(default=list, null=True, verbose_name='Values')

    def __str__(self):
        return self.name


class AttributeGroup(BaseModel):
    name = models.CharField(max_length=75, null=True, verbose_name='Name')
    attributes = models.ManyToManyField(Attribute, related_name='attributeitems', null=True, verbose_name='Attributes')

    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(max_length=75, blank=True, null=True, verbose_name='Name', db_index=True)
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    handle = models.CharField(max_length=75, blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='Active')

    parent_category = models.ForeignKey(
        'Category', related_name='subcategory', verbose_name='Parent Category',
        on_delete=models.SET_NULL, blank=True, null=True
    )

    second_parent_category = models.ForeignKey(
        'Category', related_name='secondsubcategory', verbose_name='Second Parent Category',
        on_delete=models.SET_NULL, blank=True, null=True
    )

    attribute_group = models.ForeignKey(
        AttributeGroup, related_name='attributegroup', verbose_name='Attribute Groups',
        on_delete=models.SET_NULL, blank=True, null=True
    )

    tags = models.ManyToManyField(
        Tag, related_name='category_tags', verbose_name='Tags', blank=True, null=True
    )

    def __str__(self):
        return self.name


class Dimension(BaseModel):
    DIMENSION_UNIT = (
        ('mm', 'mm'),
        ('cm', 'cm'),
        ('inch', 'inch'),
        ('M', 'M'),
    )

    WEIGHT_UNIT = (
        ('gm', 'gm'),
        ('Kg', 'Kg'),
    )

    length = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Length')
    breadth = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Breadth')
    height = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Height')

    dimension_unit = models.CharField(max_length=20, choices=DIMENSION_UNIT, verbose_name='Dimension Unit', null=True,
                                      blank=True)

    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Weight')
    weight_unit = models.CharField(max_length=20, choices=WEIGHT_UNIT, verbose_name='Weight Unit', null=True,
                                   blank=True)
