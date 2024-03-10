from rest_framework import serializers

from masterdata.models import Category
from masterdata.models import Brand
from masterdata.models import Tag
from masterdata.models import Attribute
from masterdata.models import AttributeGroup
from masterdata.models import Dimension


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BrandModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class TagModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class AttributeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = (
            'name',
            'value',
        )


class AttributeGroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeGroup
        fields = (
            'name',
            'attributes',
        )


class DimensionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dimension
        fields = (
            'length',
            'breadth',
            'height',
            'dimension_unit',
            'weight',
            'weight_unit',
        )
