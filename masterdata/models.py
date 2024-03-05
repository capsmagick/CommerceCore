from django.db import models
from setup.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=75, blank=True, null=True, verbose_name='Name', db_index=True)
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    handle = models.CharField(max_length=75, blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='Active')
    parent_category = models.ForeignKey(
        'Category', related_name='subcategory', verbose_name='Parent Category',
        on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.name


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
