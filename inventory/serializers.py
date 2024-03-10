from rest_framework import serializers


from inventory.models import Tax
from inventory.models import Warehouse
from inventory.models import Batch
from inventory.models import Inventory


class TaxModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = '__all__'


class WarehouseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class BatchModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = '__all__'


class InventoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'
