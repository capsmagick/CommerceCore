from rest_framework import serializers


from inventory.models import Tax
from inventory.models import Warehouse
from inventory.models import Batch
from inventory.models import Inventory


class TaxModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'

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


class WarehouseModelSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Inventory
        fields = '__all__'
