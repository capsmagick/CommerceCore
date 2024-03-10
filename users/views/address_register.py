from setup.views import BaseModelViewSet
from users.models.other import AddressRegister
from users.serializers import AddressRegisterModelSerializer


class AddressRegisterModelViewSet(BaseModelViewSet):
    queryset = AddressRegister.objects.all()
    serializer_class = AddressRegisterModelSerializer
    default_fields = [
        'user',
        'full_name', 'contact_number', 'alternative_contact_number',
        'address_line_1', 'address_line_2', 'land_mark',
        'district', 'state', 'country', 'pin_code', 'address_type', 'is_default'
    ]