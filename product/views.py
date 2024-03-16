from setup.views import BaseModelViewSet

from product.models import Products
from product.models import Variant
from product.models import ProductImage
from product.models import Collection
from product.models import LookBook

from product.serializers import ProductsModelSerializer
from product.serializers import VariantModelSerializer
from product.serializers import VariantModelSerializerGET
from product.serializers import ProductImageModelSerializer
from product.serializers import CollectionModelSerializer
from product.serializers import LookBookModelSerializer

from setup.utils import compress_image


class ProductsModelViewSet(BaseModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsModelSerializer
    search_fields = ['name']
    default_fields = [
        'name',
        'short_description',
        'description',
        'sku',
        'price',
        'selling_price',
        'condition',
        'categories',
        'brand',
        'is_disabled',
        'hsn_code',
        'rating',
        'no_of_reviews',
        'tags',
        'dimension'
    ]


class VariantModelViewSet(BaseModelViewSet):
    queryset = Variant.objects.all()
    serializer_class = VariantModelSerializer
    retrieve_serializer_class = VariantModelSerializerGET
    search_fields = ['product__name']
    default_fields = [
        'product',
        'attributes'
    ]


class ProductImageModelViewSet(BaseModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageModelSerializer
    search_fields = ['product__name']
    default_fields = [
        'product',
        'variant',
        'image',
        'thumbnail',
        'alt_text'
    ]

    def perform_db_action(self, serializer):
        obj = serializer.save()

        if obj.image:
            compressed_image = compress_image(serializer.validated_data['image'])
            try:
                # obj.thumbnail = compressed_image
                obj.thumbnail.save(f"thumbnail_{obj.image.name}", compressed_image)
                obj.save()
            except Exception as e:
                print('Exception e : ', str(e))


class CollectionModelViewSet(BaseModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionModelSerializer
    search_fields = ['name']
    default_fields = [
        'name',
        'collections'
    ]


class LookBookModelViewSet(BaseModelViewSet):
    queryset = LookBook.objects.all()
    serializer_class = LookBookModelSerializer
    search_fields = ['name']
    default_fields = [
        'name',
        'variants'
    ]

