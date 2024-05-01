from rest_framework import serializers


from inventory.models import Tax
from inventory.models import Warehouse
from inventory.models import Batch
from inventory.models import Inventory


class TaxModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = (
            'name',
            'slab',
        )

    def validate(self, attrs):
        name = attrs.get('name')

        if not self.instance:
            if Tax.objects.filter(name=name).exists():
                raise serializers.ValidationError({
                    'name': 'Name is already in use.'
                })

        else:
            if name != self.instance.name:
                if Tax.objects.filter(name=name).exists():
                    raise serializers.ValidationError({
                        'name': 'Name is already in use.'
                    })

        return attrs


class TaxModelSerializerGET(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    class Meta:
        model = Tax
        fields = '__all__'


class WarehouseModelSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    class Meta:
        model = Warehouse
        fields = '__all__'

    def validate(self, attrs):
        name = attrs.get('name')

        if not self.instance:
            if Warehouse.objects.filter(name=name).exists():
                raise serializers.ValidationError({
                    'name': 'Name is already in use.'
                })

        else:
            if name != self.instance.name:
                if Warehouse.objects.filter(name=name).exists():
                    raise serializers.ValidationError({
                        'name': 'Name is already in use.'
                    })

        return attrs


class BatchModelSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    class Meta:
        model = Batch
        fields = '__all__'

    def validate(self, attrs):
        batch_number = attrs.get('batch_number')

        if not self.instance:
            if Batch.objects.filter(batch_number=batch_number).exists():
                raise serializers.ValidationError({
                    'name': 'Batch Number is already in use.'
                })

        else:
            if batch_number != self.instance.name:
                if Batch.objects.filter(batch_number=batch_number).exists():
                    raise serializers.ValidationError({
                        'name': 'Batch Number is already in use.'
                    })

        return attrs


class InventoryModelSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, attrs):
        return str(attrs.created_by if attrs.created_by else '')

    def get_updated_by(self, attrs):
        return str(attrs.updated_by if attrs.updated_by else '')

    class Meta:
        model = Inventory
        fields = '__all__'
