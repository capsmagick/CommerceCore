from setup.views import BaseModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

import openpyxl
import psycopg2



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


class ImportProduct(APIView):

    def post(self, request):
        file = request.FILES.get('import_file')
        print('File: ', file)


        wb = openpyxl.load_workbook(file)
        sheet = wb.active

        for row in sheet.iter_rows(values_only=True):
            print('--------------------------------------------')
            print('row : ', row)
            print('--------------------------------------------')


        return Response({
            'message': 'Success'
        }, status=status.HTTP_200_OK)
