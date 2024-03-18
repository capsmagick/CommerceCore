from rest_framework import serializers

from product.models import Products
from product.models import Variant
from product.models import ProductImage
from product.models import Collection
from product.models import LookBook


class ProductsModelSerializer(serializers.ModelSerializer):
    from customer.serializers import ReviewSerializer
    review = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Products
        fields = '__all__'

    def validate(self, attrs):
        name = attrs.get('name')

        if not self.instance:
            if Products.objects.filter(name=name).exists():
                raise serializers.ValidationError({
                    'name': 'Name is already in use.'
                })

        else:
            if name != self.instance.name:
                if Products.objects.filter(name=name).exists():
                    raise serializers.ValidationError({
                        'name': 'Name is already in use.'
                    })

        return attrs


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
    image = serializers.ImageField()

    class Meta:
        model = ProductImage
        fields = '__all__'


class CollectionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

    def validate(self, attrs):
        name = attrs.get('name')

        if not self.instance:
            if Collection.objects.filter(name=name).exists():
                raise serializers.ValidationError({
                    'name': 'Name is already in use.'
                })

        else:
            if name != self.instance.name:
                if Collection.objects.filter(name=name).exists():
                    raise serializers.ValidationError({
                        'name': 'Name is already in use.'
                    })

        return attrs


class LookBookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LookBook
        fields = '__all__'

    def validate(self, attrs):
        name = attrs.get('name')

        if not self.instance:
            if LookBook.objects.filter(name=name).exists():
                raise serializers.ValidationError({
                    'name': 'Name is already in use.'
                })

        else:
            if name != self.instance.name:
                if LookBook.objects.filter(name=name).exists():
                    raise serializers.ValidationError({
                        'name': 'Name is already in use.'
                    })

        return attrs
