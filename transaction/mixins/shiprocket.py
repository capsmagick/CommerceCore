import requests
from django.conf import settings


class Shiprocket:

    GENERATE_TOKEN = 'https://apiv2.shiprocket.in/v1/external/auth/login/'
    CREATE_ORDER = 'https://apiv2.shiprocket.in/v1/external/orders/create/adhoc/'
    UPDATE_CUSTOMER_DELIVERY_ADDRESS = 'https://apiv2.shiprocket.in/v1/external/orders/address/update/'
    UPDATE_ORDER = 'https://apiv2.shiprocket.in/v1/external/orders/update/adhoc/'
    CANCEL_ORDER = 'https://apiv2.shiprocket.in/v1/external/orders/cancel/'

    COURIER_LIST = 'https://apiv2.shiprocket.in/v1/external/courier/serviceability/'

    ALL_ORDER = 'https://apiv2.shiprocket.in/v1/external/orders/'
    ORDER_DETAILS = 'https://apiv2.shiprocket.in/v1/external/orders/show/{}/'
    EXPORT_ORDERS = 'https://apiv2.shiprocket.in/v1/external/orders/export/'

    def __init__(self):
        self.email = settings.SHIPROCKET_EMAIL
        self.password = settings.SHIPROCKET_PASSWORD
        self.headers = { "Content-Type": 'application/json' }

        self.authorize()

    def authorize(self):
        params = {
            "email": self.email,
            "password": self.password
        }

        response = requests.post(
            self.GENERATE_TOKEN,
            data=params,
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



