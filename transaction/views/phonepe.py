import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from django.shortcuts import render

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from setup.export import ExportData
from setup.permissions import IsCustomer
from setup.permissions import IsSuperUser

from transaction.models import Transaction
from transaction.serializers import TransactionSerializer
from transaction.serializers import TransactionRetrieveSerializer
from transaction.filters import TransactionFilter
from transaction.mixins import PhonePe


class TransactionAPIView(APIView):
    permission_classes = (IsAuthenticated, IsCustomer)
    serializer_class = TransactionSerializer

    def post(self, request, *args, **kwargs):
        """
            API For Payment Initiating

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
                order (int): The primary key of the Order model.

            Returns:
                Response: A DRF Response object indicating success or failure and a message with payment request details.
        """

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        order = serializer.validated_data.get('order')

        order.cart.complete_cart()
        order.order_payment()
        order.save()

        payment_payload = PhonePe().payment(order)

        return Response({
            'payload': payment_payload,
            'message': 'successfully initiated payment.'
        }, status=status.HTTP_200_OK)


class TransactionCallBackAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """
            API For Payment Callback by Payment Partner

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.

            Returns:
                Response: A Template Response object indicating success or failure and a message with payment request details.
        """
        form_data = request.data
        transaction_id = form_data.get('transactionId', None)

        print('------------------------------------------')
        print('form_data : ', form_data)
        print('------------------------------------------')

        if transaction_id:
            response = PhonePe().check_payment_status(transaction_id)
            print('response : ', response.status_code)
            print('response : ', response.text)
            print('response : ', response.json())

            if response.status_code == 200:
                obj = Transaction.objects.get(transaction_id=transaction_id)
                obj.status = "Success"
                try:
                    obj.response = response.json()
                except Exception as e:
                    obj.response = response.text
                obj.response_received_date = datetime.datetime.now()
                obj.save()
                obj.order.order_placed()
                obj.order.save()
                return render(request, 'payment_success.html', context={'output': response.text, 'main_request': form_data})

            else:
                obj = Transaction.objects.get(transaction_id=transaction_id)
                obj.status = "Failed"
                try:
                    obj.response = response.json()
                except Exception as e:
                    obj.response = response.text
                obj.response_received_date = datetime.datetime.now()
                obj.order.order_pending()
                obj.order.save()
                obj.save()
                return render(request, 'payment_failed.html', context={'output': response.text, 'main_request': form_data})

        return render(request, 'payment_failed.html', context={'output': 'response.text', 'main_request': form_data})


class TransactionModelViewSet(GenericViewSet, ListModelMixin, ExportData):
    """
        API For Transaction List
    """
    permission_classes = (IsAuthenticated, IsSuperUser,)
    queryset = Transaction.objects.all()
    serializer_class = TransactionRetrieveSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = TransactionFilter
    search_fields = ['transaction_id', 'status', 'order__user']




