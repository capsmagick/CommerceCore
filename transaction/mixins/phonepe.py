import requests
from django.conf import settings
from transaction.utils import base64_encode
from transaction.utils import calculate_sha256_string

from transaction.models import Transaction


class PhonePe:
    """
        Mixin for Phone pe payment gateway
    """
    MERCHANT_KEY = settings.MERCHANT_KEY
    API_KEY = settings.API_KEY
    KEY_INDEX = settings.KEY_INDEX
    REDIRECT_URL = settings.PHONE_PAY_REDIRECT_URL
    S2S_CALLBACK_URL = settings.PHONE_PAY_S2S_CALLBACK_URL
    USER_ID = settings.USER_ID

    CHECK_SUM_FORMAT = '{}###{}'

    POST_ACTION_URL = 'https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay'
    GET_ACTION_URL = 'https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/status/PGTESTPAYUAT/{}'


    def generate_headers(self, input_string):
        sha256_value = calculate_sha256_string(input_string)
        check_sum = self.CHECK_SUM_FORMAT.format(sha256_value, self.KEY_INDEX)

        headers = {
            'Content-Type': 'application/json',
            'X-VERIFY': check_sum,
            'accept': 'application/json',
        }

        return headers

    def make_request(self, transaction):
        payload = {
            "merchantId": self.MERCHANT_KEY,
            "merchantTransactionId": transaction.transaction_id,
            "merchantUserId": self.USER_ID,
            "amount": str(transaction.amount),
            "redirectUrl": self.REDIRECT_URL,
            "redirectMode": "POST",
            "callbackUrl": self.S2S_CALLBACK_URL,
            "mobileNumber": transaction.order.address.contact_number,
            "paymentInstrument": {
                "type": "PAY_PAGE"
            }
        }

        base64_string = base64_encode(payload)
        main_string = base64_string + '/pg/v1/pay' + self.API_KEY

        headers = self.generate_headers(main_string)

        response = requests.post(
            self.POST_ACTION_URL,
            headers=headers,
            data={ 'request': base64_string }
        )

        return response.json()

    def payment(self, order):
        transaction = Transaction.create_transaction(order)
        return self.make_request(transaction)

    def check_payment_status(self, transaction_id):
        request_url = self.GET_ACTION_URL.format('transaction_id')

        sha256_pay_load_string = '/pg/v1/status/PGTESTPAYUAT/' + transaction_id + self.API_KEY

        headers = self.generate_headers(sha256_pay_load_string)
        headers['X-MERCHANT-ID'] = transaction_id

        response = requests.get(request_url, headers=headers)

        return response









