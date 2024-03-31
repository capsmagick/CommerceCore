from rest_framework import serializers

from .models import Category
from .models import Brand
from .models import Tag
from .models import Attribute
from .models import AttributeGroup
from .models import Dimension
from .models import ReturnReason


class BrandModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = (
            'created_by',
            'created_at',
            'updated_by',
            'updated_at',
            'deleted',
            'deleted_at',
            'deleted_by',
        )
    
    def validate(self, attrs):
        name = attrs.get('name')

        if not self.instance:
            if Brand.objects.filter(name=name).exists():
                raise serializers.ValidationError({
                    'name': 'Name is already in use.'
                })

        else:
            if name != self.instance.name:
                if Brand.objects.filter(name=name).exists():
                    raise serializers.ValidationError({
                        'name': 'Name is already in use.'
                    })

        return attrs


class BrandModelSerializerGET(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class TagModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

    def validate(self, attrs):
        name = attrs.get('name')

        if not self.instance:
            if Tag.objects.filter(name=name).exists():
                raise serializers.ValidationError({
                    'name': 'Name is already in use.'
                })

        else:
            if name != self.instance.name:
                if Tag.objects.filter(name=name).exists():
                    raise serializers.ValidationError({
                        'name': 'Name is already in use.'
                    })

        return attrs


class AttributeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = (
            'name',
            'value',
        )

    def validate(self, attrs):
        name = attrs.get('name')

        if not self.instance:
            if Attribute.objects.filter(name=name).exists():
                raise serializers.ValidationError({
                    'name': 'Name is already in use.'
                })

        else:
            if name != self.instance.name:
                if Attribute.objects.filter(name=name).exists():
                    raise serializers.ValidationError({
                        'name': 'Name is already in use.'
                    })

        return attrs


class RetrieveAttributeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'


class AttributeGroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeGroup
        fields = (
            'name',
            'attributes',
        )

    def validate(self, attrs):
        name = attrs.get('name')

        if not self.instance:
            if AttributeGroup.objects.filter(name=name).exists():
                raise serializers.ValidationError({
                    'name': 'Name is already in use.'
                })

        else:
            if name != self.instance.name:
                if AttributeGroup.objects.filter(name=name).exists():
                    raise serializers.ValidationError({
                        'name': 'Name is already in use.'
                    })

        return attrs


class RetrieveAttributeGroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeGroup
        fields = '__all__'


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


class RetrieveDimensionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dimension
        fields = '__all__'


class CategoryModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

    def validate(self, attrs):
        name = attrs.get('name')

        if not self.instance:
            if Category.objects.filter(name=name).exists():
                raise serializers.ValidationError({
                    'name': 'Name is already in use.'
                })

        else:
            if name != self.instance.name:
                if Category.objects.filter(name=name).exists():
                    raise serializers.ValidationError({
                        'name': 'Name is already in use.'
                    })

        return attrs


class CategoryModelSerializerGET(serializers.ModelSerializer):
    tags = TagModelSerializer(many=True)

    class Meta:
        model = Category
        fields = '__all__'


class ReturnReasonModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReturnReason
        fields = (
            'title',
            'description',
        )


class ReturnReasonModelSerializerGET(serializers.ModelSerializer):
    class Meta:
        model = ReturnReason
        fields = '__all__'

