from rest_framework import serializers

from product.models import Products
from product.models import Variant
from product.models import VariantAttributes
from product.models import ProductImage
from product.models import Collection
from product.models import CollectionItems
from product.models import LookBook
from product.models import LookBookItems

from customer.models import WishList

from customer.serializers.serializers import ReviewSerializer
from masterdata.serializers import CategoryGET
from masterdata.serializers import BrandModelSerializerGET
from masterdata.serializers import RetrieveDimensionModelSerializer
from masterdata.serializers import RetrieveAttributeModelSerializer


class ProductsModelSerializer(serializers.ModelSerializer):
    short_description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=1.00)
    selling_price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=1.00)
    condition = serializers.CharField(required=False, default='New')
    images = serializers.ListField(
        child=serializers.FileField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True, required=False
    )
    tags = serializers.ListField(child=serializers.CharField(), required=False, allow_null=True, allow_empty=True)

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

        product = Products.objects.create(**validated_data)

        if categories:
            product.categories.set(categories)

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
    categories = CategoryGET(many=True, read_only=True)
    brand = BrandModelSerializerGET(read_only=True)
    dimension = RetrieveDimensionModelSerializer(read_only=True)
    images = serializers.SerializerMethodField()

    def get_images(self, attrs):
        return ProductImageModelSerializer(attrs.product_images.all(), many=True).data

    class Meta:
        model = Products
        fields = '__all__'


class VariantModelSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(min_value=1)
    selling_price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=1.00)
    images = serializers.ListField(
        child=serializers.FileField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True, required=False
    )
    attributes = serializers.JSONField(required=True, write_only=True)

    def create(self, validated_data):
        from setup.utils import compress_image
        attachment = validated_data.pop('images', [])
        attributes = validated_data.pop('attributes', None)
        product = Variant.objects.create(**validated_data)

        if attributes:
            for i in attributes:
                product.variant.create(**{
                    'attributes_id': i['attribute'],
                    'value': i['value']
                })

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
    product = ProductsModelSerializerGET()
    attributes = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    wish_listed = serializers.SerializerMethodField()

    def get_attributes(self, attrs):
        return VariantAttributeModelSerializerGET(attrs.variant.all(), many=True).data

    def get_wish_listed(self, attrs):
        from setup.middleware.request import CurrentRequestMiddleware
        request = CurrentRequestMiddleware.get_request()
        return WishList.objects.filter(product_variant_id=attrs.id, user_id=request.user.id).exists()

    def get_images(self, attrs):
        return ProductImageModelSerializer(attrs.variant_images.all(), many=True).data

    class Meta:
        model = Variant
        fields = '__all__'


class VariantAttributeModelSerializerGET(serializers.ModelSerializer):
    attributes = RetrieveAttributeModelSerializer()

    class Meta:
        model = VariantAttributes
        fields = '__all__'


class ProductImageModelSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = ProductImage
        fields = '__all__'


class CollectionModelSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(), required=False, allow_null=True, allow_empty=True)

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


class CollectionModelSerializerGET(serializers.ModelSerializer):
    feature_image = serializers.SerializerMethodField()
    collection_items = serializers.SerializerMethodField()

    def get_collection_items(self, attrs):
        return CollectionItemsModelSerializerGET(attrs.collection_items.all(), many=True).data

    def get_feature_image(self, attrs):
        return attrs.feature_image.url if attrs.feature_image else ''

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
            'is_in_home_page',
        )


class LookBookModelSerializerGET(serializers.ModelSerializer):
    look_book_items = serializers.SerializerMethodField()

    def get_look_book_items(self, attrs):
        return LookBookItemsModelSerializerGET(attrs.look_book_items.all(), many=True).data

    class Meta:
        model = LookBook
        fields = '__all__'


class AddToCollectionSerializer(serializers.Serializer):
    collection = serializers.PrimaryKeyRelatedField(
        queryset=Collection.objects.all()
    )


class AddToLookBookSerializer(serializers.Serializer):
    look_book = serializers.PrimaryKeyRelatedField(
        queryset=LookBook.objects.all()
    )


class AddProductCollectionSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Products.objects.all()
    )


class CollectionItemsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionItems
        fields = (
            'collection',
            'product',
        )


class CollectionItemsModelSerializerGET(serializers.ModelSerializer):
    product = ProductsModelSerializerGET(read_only=True)

    class Meta:
        model = CollectionItems
        fields = '__all__'


class LookBookItemsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LookBookItems
        fields = (
            'look_book',
            'product',
        )


class LookBookItemsModelSerializerGET(serializers.ModelSerializer):
    product = ProductsModelSerializerGET(read_only=True)

    class Meta:
        model = LookBookItems
        fields = '__all__'


