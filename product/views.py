from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from setup.views import BaseModelViewSet
from setup.export import ExportData
from setup.utils import compress_image

from product.models import Products
from product.models import Variant
from product.models import ProductImage
from product.models import Collection
from product.models import CollectionItems
from product.models import LookBook
from product.models import LookBookItems

from product.serializers import ProductsModelSerializer
from product.serializers import ProductsModelSerializerGET
from product.serializers import VariantModelSerializer
from product.serializers import VariantModelSerializerGET
from product.serializers import ProductImageModelSerializer
from product.serializers import CollectionModelSerializer
from product.serializers import CollectionModelSerializerGET
from product.serializers import CollectionItemsModelSerializer
from product.serializers import CollectionItemsModelSerializerGET
from product.serializers import LookBookItemsModelSerializer
from product.serializers import LookBookItemsModelSerializerGET
from product.serializers import LookBookModelSerializer
from product.serializers import LookBookModelSerializerGET
from product.serializers import AddToCollectionSerializer
from product.serializers import AddToLookBookSerializer
from product.serializers import AddProductCollectionSerializer

from product.filters import ProductFilter
from product.filters import VariantFilter
from product.filters import ProductImageFilter
from product.filters import CollectionFilter
from product.filters import LookBookFilter
from product.filters import CollectionItemsFilter
from product.filters import LookBookItemsFilter


class ProductsModelViewSet(BaseModelViewSet, ExportData):
    queryset = Products.objects.all()
    serializer_class = ProductsModelSerializer
    retrieve_serializer_class = ProductsModelSerializerGET
    filterset_class = ProductFilter
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

    @action(detail=True, methods=['POST'], url_path='disable')
    def disable(self, request, *args, **kwargs):
        """
            API For disable the product

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
                pk (int): The primary key of the product table

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """
        obj = self.get_object()
        obj.disable()

        return Response({
            'message': f'{obj.name} successfully disabled.!'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='enable')
    def enable(self, request, *args, **kwargs):
        """
            API For enable the product

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
                pk (int): The primary key of the product table

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """
        obj = self.get_object()
        obj.enable()

        return Response({
            'message': f'{obj.name} successfully enabled.!'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='add-to-collection', serializer_class=AddToCollectionSerializer)
    def add_to_collection(self, request, *args, **kwargs):
        """
            API For Add the product to the collection

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
                pk (int): The primary key of the product table

            Data:
                collection (int): The primary key of the collection table

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """
        obj = self.get_object()
        serializer = AddToCollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        collection = serializer.validated_data.get('collection')

        try:
            product, created = CollectionItems.objects.get_or_create(collection_id=collection, product=obj)
        except CollectionItems.MultipleObjectsReturned:
            return Response({
                'message': f'{obj.name} already added to the collection.!'
            }, status=status.HTTP_200_OK)

        return Response({
            'message': f'{obj.name} successfully added to the collection.!'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='add-to-lookbook', serializer_class=AddToLookBookSerializer)
    def add_to_look_book(self, request, *args, **kwargs):
        """
            API For Add the product to the lookbook

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
                pk (int): The primary key of the product table

            Data:
                collection (int): The primary key of the collection table

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """
        obj = self.get_object()
        serializer = AddToLookBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        look_book = serializer.validated_data.get('look_book')
        try:
            product, created = LookBookItems.objects.get_or_create(look_book=look_book, product=obj)
        except LookBookItems.MultipleObjectsReturned:
            return Response({
                'message': f'{obj.name} already added to the look book.!'
            }, status=status.HTTP_200_OK)

        return Response({
            'message': f'{obj.name} successfully added to the look book.!'
        }, status=status.HTTP_200_OK)


class VariantModelViewSet(BaseModelViewSet):
    queryset = Variant.objects.all()
    serializer_class = VariantModelSerializer
    retrieve_serializer_class = VariantModelSerializerGET
    search_fields = ['product__name']
    default_fields = [
        'product',
        'attributes'
    ]
    filterset_class = VariantFilter

    @action(detail=True, methods=['PUT'])
    def update_record(self, request, *args, **kwargs):
        """
            Update an existing variant record

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.

            Returns:
                Response: A DRF Response object with the update status.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        attributes = serializer.validated_data.pop('attributes', None)
        obj = self.perform_db_action(serializer)

        if attributes:
            for i in attributes:
                attribute_instance = i.get('id', None)

                if attribute_instance:
                    attribute = obj.variant.get(pk=attribute_instance)
                    attribute.attributes_id = i['attribute']
                    attribute.value = i['value']
                    attribute.save()
                else:
                    obj.variant.create(**{
                        'attributes': i['attributes'],
                        'value': i['value'],
                    })
        return Response(
            {
                'data': serializer.data,
                'message': 'Successfully Updated'
            },
            status=status.HTTP_200_OK
        )


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
    filterset_class = ProductImageFilter

    def perform_db_action(self, serializer, action='create'):
        obj = serializer.save()

        if obj.image:
            compressed_image = compress_image(serializer.validated_data['image'])
            try:
                # obj.thumbnail = compressed_image
                obj.thumbnail.save(f"thumbnail_{obj.image.name}", compressed_image)
                obj.save()
            except Exception as e:
                print('Exception e : ', str(e))


class CollectionModelViewSet(BaseModelViewSet, ExportData):
    queryset = Collection.objects.all()
    serializer_class = CollectionModelSerializer
    retrieve_serializer_class = CollectionModelSerializerGET
    search_fields = ['name']
    default_fields = [
        'name',
        'collections'
    ]
    filterset_class = CollectionFilter

    @action(detail=True, methods=['POST'], url_path='add-product', serializer_class=AddProductCollectionSerializer)
    def add_product(self, request, *args, **kwargs):
        """
            API For Add the product to the collection

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
                pk (int): The primary key of the collection table

            Data:
                product (int): The primary key of the product table

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """
        obj = self.get_object()
        serializer = AddProductCollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data.get('product')
        try:
            product_obj, created = CollectionItems.objects.get_or_create(collection=obj, product=product)
        except CollectionItems.MultipleObjectsReturned:
            return Response({
                'message': f'{product.name} already added to the collection.!'
            }, status=status.HTTP_200_OK)

        return Response({
            'message': f'{product.name} successfully added to the collection.!'
        }, status=status.HTTP_200_OK)


class CollectionItemsModelViewSet(BaseModelViewSet):
    queryset = CollectionItems.objects.all()
    serializer_class = CollectionItemsModelSerializer
    retrieve_serializer_class = CollectionItemsModelSerializerGET
    search_fields = ['product__name', 'collection__name']
    default_fields = [
        'collection',
        'product',
    ]
    filterset_class = CollectionItemsFilter


class LookBookModelViewSet(BaseModelViewSet, ExportData):
    queryset = LookBook.objects.all()
    serializer_class = LookBookModelSerializer
    retrieve_serializer_class = LookBookModelSerializerGET
    search_fields = ['name']
    default_fields = [
        'name',
        'variants'
    ]
    filterset_class = LookBookFilter

    @action(detail=True, methods=['POST'], url_path='add-product', serializer_class=AddProductCollectionSerializer)
    def add_product(self, request, *args, **kwargs):
        """
            API For Add the product to the loo book

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
                pk (int): The primary key of the collection table

            Data:
                product (int): The primary key of the product table

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """
        obj = self.get_object()
        serializer = AddProductCollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data.get('product')
        try:
            product_obj, created = LookBookItems.objects.get_or_create(look_book=obj, product=product)
        except LookBookItems.MultipleObjectsReturned:
            return Response({
                'message': f'{product.name} already added to the look book.!'
            }, status=status.HTTP_200_OK)

        return Response({
            'message': f'{product.name} successfully added to the look book.!'
        }, status=status.HTTP_200_OK)


class LookBookItemsModelViewSet(BaseModelViewSet):
    queryset = LookBookItems.objects.all()
    serializer_class = LookBookItemsModelSerializer
    retrieve_serializer_class = LookBookItemsModelSerializerGET
    search_fields = ['product__name', 'look_book__name']
    default_fields = ['look_book', 'product']
    filterset_class = LookBookItemsFilter

