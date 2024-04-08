from rest_framework.viewsets import ViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from transaction.mixins import Shiprocket


class ShiprocketViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=['GET'], url_path='orders')
    def order_list(self, request, *args, **kwargs):
        data = Shiprocket().get_all_orders()
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='order/(?P<order>.*?)/details')
    def order_details(self, request, order, *args, **kwargs):
        data = Shiprocket().get_order_details(order)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='shipments')
    def shipment_list(self, request, *args, **kwargs):
        data = Shiprocket().get_all_shipment()
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='shipment/(?P<shipment>.*?)/details')
    def shipment_details(self, request, shipment, *args, **kwargs):
        data = Shiprocket().get_shipment_details(shipment)
        return Response(data, status=status.HTTP_200_OK)


class ShiprocketUtility:

    def create_order(self, obj):
        """
            To Create payload and calling api to create order

            Parameter:
                obj (object): The object of the order.
        """

        payload = {
            'order_id': obj.order_id,
            'order_date': obj.created_at,
            'pickup_location': obj.address,
            'channel_id': '',
            'comment': '',
            'billing_customer_name': obj.address.full_name,
            'billing_last_name': '',
            'billing_address': "{},{}".format(obj.address.address_line_1, obj.address.address_line_1),
            'billing_address_2': '',
            'billing_city': obj.address.district,
            'billing_pincode': obj.address.pin_code,
            'billing_state': obj.address.state,
            'billing_country': obj.address.country,
            'billing_email': obj.address.user.email,
            'billing_phone': obj.address.contact_number,
            'shipping_is_billing': 'true',
            'shipping_customer_name': "",
            'shipping_last_name': "",
            'shipping_address': "",
            'shipping_address_2': "",
            'shipping_city': "",
            'shipping_pincode': "",
            'shipping_country': "",
            'shipping_state': "",
            'shipping_email': "",
            'shipping_phone': "",
            'order_items': '',
            'payment_method': "Prepaid",
            'shipping_charges': 0,
            'giftwrap_charges': 0,
            'transaction_charges': 0,
            'total_discount': 0,
            'sub_total': obj.total_amount,
            'length': 10,
            'breadth': 15,
            'height': 20,
            'weight': 2.5
        }

        shiprocket = Shiprocket()

        data = shiprocket.create_order(payload)
        shipping_id = data.get('shipping_id')
        obj.shipping_id = shipping_id
        obj.save()
        shiprocket.request_for_shipment(shipping_id)
        return data



