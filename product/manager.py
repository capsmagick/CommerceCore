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
        queryset = queryset.filter(deleted=False)
        return queryset.filter(models.Q(variant__deleted=False) | models.Q(product__deleted=False))


class CollectionItemsManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(deleted=False, collection__deleted=False, product__deleted=False)


class LooBookItemsManager(models.Manager):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(deleted=False, look_book__deleted=False, product__deleted=False)


