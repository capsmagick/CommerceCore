from rest_framework import serializers

from product.models import Products
from product.models import Variant
from product.models import ProductImage
from product.models import Collection
from product.models import LookBook

from customer.serializers.serializers import ReviewSerializer
from masterdata.serializers import TagModelSerializer
from masterdata.serializers import CategoryModelSerializerGET
from masterdata.serializers import BrandModelSerializerGET
from masterdata.serializers import RetrieveDimensionModelSerializer


class ProductsModelSerializer(serializers.ModelSerializer):
    short_description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=1.00)
    selling_price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=1.00)
    condition = serializers.CharField(required=False, default='New')
    images = serializers.ListField(
        child=serializers.FileField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True, required=False
    )

    def validate(self, attrs):
        name = attrs.get('name')
        images = attrs.get('images')

        print('----------------------------------')
        print('images : ', images)
        print('----------------------------------')

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

    class Meta:
        model = Products
        exclude = (
            'created_by',
            'created_at',
            'updated_by',
            'updated_at',
            'deleted',
            'deleted_at',
            'deleted_by',
        )

    def create(self, validated_data):
        from setup.utils import compress_image
        attachment = validated_data.pop('images', [])

        categories = validated_data.pop('categories', None)
        tags = validated_data.pop('tags', None)

        product = Products.objects.create(**validated_data)

        if categories:
            product.categories.set(categories)

        if tags:
            product.tags.set(tags)

        print('------------------------------------')
        print('attachment : ', attachment)
        print('------------------------------------')

        for file in attachment:
            compressed_image = compress_image(file)

            img_obj = product.product_images.create(**{
                'image': file,
                'name': file.name,
            })
            img_obj.thumbnail.save(f"thumbnail_{file.name}", compressed_image)
            img_obj.save()

        return product


class ProductsModelSerializerGET(serializers.ModelSerializer):
    review = ReviewSerializer(many=True, read_only=True)
    categories = CategoryModelSerializerGET(many=True, read_only=True)
    brand = BrandModelSerializerGET(read_only=True)
    dimension = RetrieveDimensionModelSerializer(read_only=True)
    images = serializers.SerializerMethodField()
    tags = TagModelSerializer(many=True, read_only=True)

    def get_images(self, attrs):
        return ProductImageModelSerializer(attrs.product_images.all(), many=True).data

    class Meta:
        model = Products
        fields = '__all__'


class VariantModelSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(min_value=1)
    selling_price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=1.00)
    images = serializers.ListSerializer(
        child=serializers.FileField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True, required=False
    )

    def create(self, validated_data):
        from setup.utils import compress_image
        attachment = validated_data.pop('images', None)
        attributes = validated_data.pop('attributes', None)
        product = Variant.objects.create(**validated_data)

        if attributes:
            product.attributes.set(attributes)

        for file in attachment:
            compressed_image = compress_image(file)

            img_obj = product.variant_images.create(**{
                'image': file,
                'name': file.name,
            })
            img_obj.thumbnail.save(f"thumbnail_{file.name}", compressed_image)
            img_obj.save()

        return product

    class Meta:
        model = Variant
        fields = (
            'product',
            'attributes',
            'stock',
            'selling_price',
            'images',
        )


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

    class Meta:
        model = Collection
        exclude = (
            'created_by',
            'created_at',
            'updated_by',
            'updated_at',
            'deleted',
            'deleted_at',
            'deleted_by',
        )

    def create(self, validated_data):

        collections = validated_data.pop('collections', None)
        tags = validated_data.pop('tags', None)

        obj = Collection.objects.create(**validated_data)

        if collections:
            obj.collections.set(collections)

        if tags:
            obj.tags.set(tags)

        return obj


class CollectionModelSerializerGET(serializers.ModelSerializer):
    collections = VariantModelSerializerGET(many=True, read_only=True)
    tags = TagModelSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = '__all__'


class LookBookModelSerializer(serializers.ModelSerializer):

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

    class Meta:
        model = LookBook
        fields = (
            'name',
            'variants',
        )

    def create(self, validated_data):
        variants = validated_data.pop('variants', None)

        obj = LookBook.objects.create(**validated_data)

        if variants:
            obj.variants.set(variants)

        return obj


class LookBookModelSerializerGET(serializers.ModelSerializer):
    variants = VariantModelSerializerGET(many=True, read_only=True)

    class Meta:
        model = LookBook
        fields = '__all__'
