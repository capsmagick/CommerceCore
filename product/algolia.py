# from algoliasearch_django import AlgoliaIndex
#
# from product.models import Products
# from product.models import Variant
#
#
# class ProductIndex(AlgoliaIndex):
#     fields = (
#     'name', 'short_description', 'description', 'sku', 'price', 'selling_price', 'condition', 'brand', 'categories',
#     'tags', 'dimension', 'rating', 'no_of_reviews')
#
#     settings = {'searchableAttributes': ['name', 'short_description', 'description', 'sku', 'brand', 'tags']}
#
#
# class VariantIndex(AlgoliaIndex):
#     fields = ('product', 'attributes', 'stock', 'selling_price')
#
#     settings = {'searchableAttributes': ['product']}
#
#
# ProductIndex.register(Products)
# VariantIndex.register(Variant)
