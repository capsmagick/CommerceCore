import requests
from django.conf import settings


class Shiprocket:
    EMAIL = settings.SHIPROCKET_EMAIL
    PASSWORD = settings.SHIPROCKET_PASSWORD

    GENERATE_TOKEN = 'https://apiv2.shiprocket.in/v1/external/auth/login'
    CREATE_ORDER = 'https://apiv2.shiprocket.in/v1/external/orders/create/adhoc'
    UPDATE_CUSTOMER_DELIVERY_ADDRESS = 'https://apiv2.shiprocket.in/v1/external/orders/address/update'
    UPDATE_ORDER = 'https://apiv2.shiprocket.in/v1/external/orders/update/adhoc'
    CANCEL_ORDER = 'https://apiv2.shiprocket.in/v1/external/orders/cancel'

    COURIER_LIST = 'https://apiv2.shiprocket.in/v1/external/courier/serviceability/'

    ALL_ORDER = 'https://apiv2.shiprocket.in/v1/external/orders'
    ORDER_DETAILS = 'https://apiv2.shiprocket.in/v1/external/orders/show'
    EXPORT_ORDERS = 'https://apiv2.shiprocket.in/v1/external/orders/export'



