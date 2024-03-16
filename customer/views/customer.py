from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from product.models import Variant

from product.serializers import VariantModelSerializerGET


class CustomerVariantViewSet(GenericViewSet, ListModelMixin):
    permission_classes = (AllowAny,)
    queryset = Variant.objects.all()
    serializer_class = VariantModelSerializerGET



