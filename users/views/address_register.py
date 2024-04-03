from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from setup.permissions import IsCustomer
from setup.views import BaseModelViewSet
from users.models.other import AddressRegister
from users.serializers import AddressRegisterModelSerializer
from users.serializers import AddressRegisterModelSerializerGET
from users.filters import AddressRegisterFilter


class AddressRegisterModelViewSet(BaseModelViewSet):
    permission_classes = (IsAuthenticated, IsCustomer,)
    queryset = AddressRegister.objects.all()
    serializer_class = AddressRegisterModelSerializer
    retrieve_serializer_class = AddressRegisterModelSerializerGET
    default_fields = [
        'user',
        'full_name', 'contact_number', 'alternative_contact_number',
        'address_line_1', 'address_line_2', 'land_mark',
        'district', 'state', 'country', 'pin_code', 'address_type', 'is_default'
    ]
    filterset_class = AddressRegisterFilter

    @action(detail=True, methods=['POST'], url_path='make-default')
    def make_default(self, request, *args, **kwargs):
        """
            API For marking default address in the customer address registry

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
                pk (int): The primary key of the address register table.

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """
        obj = self.get_object()
        obj.make_default()

        return Response({
            'message': f'Successfully added as default address.!'
        }, status=status.HTTP_200_OK)