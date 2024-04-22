from setup.views import BaseModelViewSet

from .models import Inventory
from .models import Batch
from .models import Tax
from .models import Warehouse

from .serializers import InventoryModelSerializer
from .serializers import BatchModelSerializer
from .serializers import TaxModelSerializer
from .serializers import TaxModelSerializerGET
from .serializers import WarehouseModelSerializer


class TaxModelViewSet(BaseModelViewSet):
    queryset = Tax.objects.all()
    serializer_class = TaxModelSerializer
    retrieve_serializer_class = TaxModelSerializerGET
    search_fields = ['name']
    default_fields = [
        'name',
        'slab'
    ]


class WarehouseModelViewSet(BaseModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseModelSerializer
    search_fields = ['name']
    default_fields = ['name']


class BatchModelViewSet(BaseModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchModelSerializer
    search_fields = ['batch_number', 'rack', 'row']
    default_fields = [
        'warehouse',
        'batch_number',
        'rack',
        'row',
        'expiry_date',
        'purchase_amount',
        'mrp',
        'selling_price',
        'purchase_quantity',
        'stock',
        'is_perishable',
        'is_disabled',
        'tax_inclusive',
        'purchase_amount_tax_inclusive',
        'tax'
    ]


class InventoryModelViewSet(BaseModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventoryModelSerializer
    search_fields = ['stock', 'batch']
    default_fields = [
        'variants',
        'stock',
        'batch',
        'low_stock_notification'
    ]
