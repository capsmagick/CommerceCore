import requests
import json
from django.conf import settings


class ShipRocket:

    GENERATE_TOKEN = 'https://apiv2.shiprocket.in/v1/external/auth/login/'

    CREATE_ORDER = 'https://apiv2.shiprocket.in/v1/external/orders/create/adhoc/'
    UPDATE_CUSTOMER_DELIVERY_ADDRESS = 'https://apiv2.shiprocket.in/v1/external/orders/address/update/'
    UPDATE_ORDER = 'https://apiv2.shiprocket.in/v1/external/orders/update/adhoc/'
    CANCEL_ORDER = 'https://apiv2.shiprocket.in/v1/external/orders/cancel/'

    GENERATE_AWB_FOR_SHIPMENT = 'https://apiv2.shiprocket.in/v1/external/courier/assign/awb/'
    REQUEST_FOR_SHIPMENT = 'https://apiv2.shiprocket.in/v1/external/courier/generate/pickup/'

    COURIER_LIST = 'https://apiv2.shiprocket.in/v1/external/courier/serviceability/'

    ALL_ORDER = 'https://apiv2.shiprocket.in/v1/external/orders/'
    ORDER_DETAILS = 'https://apiv2.shiprocket.in/v1/external/orders/show/{}/'

    ALL_SHIPMENT = 'https://apiv2.shiprocket.in/v1/external/shipments/'
    SHIPMENT_DETAILS = 'https://apiv2.shiprocket.in/v1/external/shipments/{}/'
    CANCEL_SHIPMENT = 'https://apiv2.shiprocket.in/v1/external/orders/cancel/shipment/awbs/'

    EXPORT_ORDERS = 'https://apiv2.shiprocket.in/v1/external/orders/export/'

    def __init__(self):
        self.email = settings.SHIPROCKET_EMAIL
        self.password = settings.SHIPROCKET_PASSWORD
        self.headers = {"Content-Type": 'application/json'}

        self.authorize()

    def authorize(self):
        params = {
            "email": self.email,
            "password": self.password
        }

        response = requests.post(
            self.GENERATE_TOKEN,
            data=json.dumps(params),
            headers=self.headers
        )
        response.raise_for_status()

        self.token = response.json()['token'] # noqa
        self.headers['Authorization'] = f"Bearer {self.token}"

    def get_all_orders(self):
        """
            This function is to create a new request to fetch all orders from shiprocket.
        """
        response = requests.get(
            self.ALL_ORDER,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_order_details(self, order):
        """
            This function is to create a new request to fetch order details of particular order from shiprocket.

            Parameters:
                order (Char): Order id of an order

            Returns:
                Response: A DRF Response object which returns from the shiprocket api.
        """
        response = requests.get(
            self.ORDER_DETAILS.format(order),
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_courier_list(self):
        """
            This function is to create a new request to fetch all courier from shiprocket.
        """
        response = requests.get(
            self.COURIER_LIST,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def create_order(self, payload):
        """
            This function is to create a new order in Shiprocket.

            Payload Data:
                order_id (char):
                    Required Yes
                order_date
                pickup_location
                channel_id
                comment
                reseller_name
                company_name
                billing_customer_name
                billing_last_name
                billing_address
                billing_address_2
                billing_city
                billing_pincode
                billing_state
                billing_country
                billing_email
                billing_phone
                billing_alternate_phone
                shipping_is_billing
                shipping_customer_name
                shipping_last_name
                shipping_address
                shipping_address_2
                billing_isd_code
                shipping_city
                shipping_pincode
                shipping_state
                shipping_email
                shipping_phone
                longitude
                latitude
                order_items
                name
                sku
                units
                selling_price
                discount
                tax
                hsn
                payment_method
                shipping_charges
                giftwrap_charges
                transaction_charges
                total_discount
                sub_total
                length
                breadth
                height
                weight
                ewaybill_no
                customer_gstin
                invoice_number
                order_type
                checkout_shipping_method
                what3words_address
                is_insurance_opt
        """

        response = requests.post(
            self.CREATE_ORDER,
            data=json.dumps(payload),
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def update_order(self, payload):
        """
            This function is to update the order in Shiprocket.
        """

        response = requests.post(
            self.CREATE_ORDER,
            data=json.dumps(payload),
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def update_address(self, payload):
        """
            This function is to update the address in order.
        """

        response = requests.post(
            self.CREATE_ORDER,
            data=json.dumps(payload),
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def generate_awb(self, data):
        """
            This Function is to create AWB for Shipment (It is mandatory to create AWB before request an shipment)
        """

        response = requests.post(
            self.GENERATE_AWB_FOR_SHIPMENT,
            headers=self.headers,
            data=json.dumps(data)
        )
        response.raise_for_status()
        return response.json()

    def request_for_shipment(self, shipment_id):
        """
            This function to request Ship Rocket for shipment
        """

        awb_response = self.generate_awb({'shipment_id': shipment_id})

        if awb_response:
            response = requests.post(
                self.REQUEST_FOR_SHIPMENT,
                headers=self.headers,
                data=json.dumps({'shipment_id': [shipment_id]})
            )
            response.raise_for_status()
            return response.json()

    def get_all_shipment(self):
        """
            This function is to create a new request to fetch all shipment from shiprocket.
        """
        response = requests.get(
            self.ALL_SHIPMENT,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

    def get_shipment_details(self, shipment):
        """
            This function is to create a new request to fetch shipment details of particular order from shiprocket.

            Parameters:
                shipment (Char): Order id of an order

            Returns:
                Response: A DRF Response object which returns from the shiprocket api.
        """
        response = requests.get(
            self.SHIPMENT_DETAILS.format(shipment),
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()



