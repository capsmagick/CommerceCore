from django.db import models


class ProductsManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(deleted=False, brand__deleted=False)


class VariantManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(deleted=False, product__deleted=False)


class VariantAttributesManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(deleted=False, variant__deleted=False, attributes__deleted=False)


class ProductImageManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(deleted=False, variant__deleted=False, product__deleted=False)


class CollectionItemsManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(deleted=False, collection__deleted=False, product__deleted=False)


