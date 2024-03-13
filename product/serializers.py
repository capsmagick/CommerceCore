from rest_framework import serializers

from product.models import Products
from product.models import Variant
from product.models import ProductImage
from product.models import Collection
from product.models import LookBook


class ProductsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class VariantModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'


class VariantModelSerializerGET(serializers.ModelSerializer):
    product = ProductsModelSerializer()
    class Meta:
        model = Variant
        fields = '__all__'


class ProductImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class CollectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'


class LookBookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LookBook
        fields = '__all__'
