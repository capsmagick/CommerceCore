import datetime
from rest_framework import status
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from setup.utils import generate_column
from setup.views import BaseModelViewSet
from setup.permissions import IsCustomer
from setup.permissions import IsSuperUser

from customer.models import Return

from customer.serializers import ReturnModelSerializer
from customer.serializers import ReturnModelSerializerGET
from customer.serializers import ReturnTrackingUpdateSerializer
from customer.serializers import ReturnApproveModelSerializer
from customer.serializers import ReturnRejectModelSerializer
from customer.serializers import UpdateReturnRefundDetailsModelSerializer

from customer.filters import CustomerReturnFilter


class CustomerReturnViewSet(BaseModelViewSet):
    """
        API for Return request to customer.
    """
    permission_classes = (IsAuthenticated, IsCustomer,)
    queryset = Return.objects.all()
    serializer_class = ReturnTrackingUpdateSerializer
    retrieve_serializer_class = ReturnModelSerializerGET
    filterset_class = CustomerReturnFilter
    search_fields = ['reason__title', 'product__product__name', 'refund_method', 'status', 'refund_status']

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return self.queryset.filter(created_by=user)

    @action(detail=False, methods=['POST'], url_path='add-return', serializer_class=ReturnModelSerializer)
    def create_record(self, request, *args, **kwargs):
        """
            Create a new return request

            Parameters:
            request (HttpRequest): The HTTP request object containing model data.
            reason (int): The primary key of the return reason model.
            product (int): The primary key of the variant product model.
            purchase_bill (file): The bill for the purchase.
            description (char): The comment by the customer
            refund_method (char): The customer wish that what type of the refund will be Exchange or Refund

            Returns:
            Response: A DRF Response object indicates success or a failure with a message.
        """
        serializer = ReturnModelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Successfully added return request.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['PATCH'], url_path='update-return', serializer_class=ReturnTrackingUpdateSerializer)
    def update_record(self, request, *args, **kwargs):
        """
            Update an existing return request

            Parameters:
            request (HttpRequest): The HTTP request object containing model data.
            tracking_id (char): The tracking id of product that sent by the customer.
            shipping_agent (char): The shipping agent that the customer sent the product through.

            Returns:
            Response: A DRF Response object indicates success or a failure with a message.
        """
        instance = self.get_object()
        serializer = ReturnTrackingUpdateSerializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Successfully updated return request.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class ManageCustomerReturn(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    permission_classes = (IsAuthenticated, IsSuperUser,)
    queryset = Return.objects.all()
    serializer_class = ReturnModelSerializerGET
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerReturnFilter
    search_fields = ['reason__title', 'product__product__name', 'refund_method', 'status', 'refund_status']
    default_fields = [
        'return_id',
        'reason',
        'product',
        'description',
        'tracking_id',
        'shipping_agent',
        'status',
    ]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        try:
            response.data['columns'] = generate_column(
                self.queryset.model, actions=True,
                default_fields=self.default_fields
            )
        except Exception as e:
            print('Exception occurred while generating the columns : ', e)
        return response

    @action(detail=True, methods=['PATCH'], url_path='update-refund-details', serializer_class=UpdateReturnRefundDetailsModelSerializer)
    def update_return_refund_details(self, request, *args, **kwargs):
        obj = self.get_object()

        serializer = UpdateReturnRefundDetailsModelSerializer(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Successfully updated return refund details.!'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='move-to-review')
    def review(self, request, *args, **kwargs):
        obj = self.get_object()

        obj.in_review()
        obj.save()

        return Response({
            'message': 'Successfully moved to In Review'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='approve', serializer_class=ReturnApproveModelSerializer)
    def approve(self, request, *args, **kwargs):
        obj = self.get_object()

        serializer = ReturnApproveModelSerializer(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_obj = serializer.save()

        updated_obj.approve()
        updated_obj.approved_at = datetime.datetime.now()
        updated_obj.approved_user = request.user
        updated_obj.refund_status = 'Pending'
        updated_obj.save()

        return Response({
            'message': 'Successfully approved return request.!'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='reject', serializer_class=ReturnRejectModelSerializer)
    def reject(self, request, *args, **kwargs):
        obj = self.get_object()

        serializer = ReturnApproveModelSerializer(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_obj = serializer.save()

        updated_obj.reject()
        updated_obj.rejected_at = datetime.datetime.now()
        updated_obj.rejected_user = request.user
        updated_obj.save()

        return Response({
            'message': 'Successfully rejected return request.!'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='move-to-intransit')
    def in_transit(self, request, *args, **kwargs):
        obj = self.get_object()

        obj.in_transit()
        obj.save()

        return Response({
            'message': 'Successfully moved to In Transit'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='move-to-delivered')
    def delivered(self, request, *args, **kwargs):
        obj = self.get_object()

        obj.delivered()
        obj.save()

        return Response({
            'message': 'Successfully moved to Delivered'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='move-to-refund-initiated')
    def refund_initiated(self, request, *args, **kwargs):
        obj = self.get_object()

        obj.refund_initiated()
        obj.save()

        return Response({
            'message': 'Successfully moved to Delivered'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='move-to-refunded')
    def refunded(self, request, *args, **kwargs):
        obj = self.get_object()

        obj.refunded()
        obj.save()

        return Response({
            'message': 'Successfully moved to Refunded'
        }, status=status.HTTP_200_OK)


