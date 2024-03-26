# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from algoliasearch_django import AlgoliaIndex
#
# from django.conf import settings
#
# from product.models import Products
# from product.models import Variant
#
# from product.algolia import ProductIndex
# from product.algolia import VariantIndex
#
#
# @receiver(post_save, sender=Products)
# def product_index_post_save(sender, instance, created, **kwargs):
#     if created:
#         index = AlgoliaIndex(model=Products, client=settings.ALGOLIA)
#         index.save_object(instance)
#     else:
#         index = AlgoliaIndex('ProductIndex')
#         index.save_object(instance)
#
#
# @receiver(post_delete, sender=Products)
# def product_index_delete(sender, instance, **kwargs):
#     index = ProductIndex(Products)
#     index.delete_object(instance.pk)
#
#
# @receiver(post_save, sender=Variant)
# def variant_index_record(sender, instance, created, **kwargs):
#     if created:
#         index = AlgoliaIndex('VariantIndex')
#         index.save_object(instance)
#     else:
#         index = AlgoliaIndex('VariantIndex')
#         index.save_object(instance)
#
#
# @receiver(post_delete, sender=Variant)
# def variant_index_delete(sender, instance, **kwargs):
#     index = AlgoliaIndex('VariantIndex')
#     index.delete_object(instance.pk)
