from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from setup.export import ExportData
from setup.permissions import IsSuperUser
from setup.utils import generate_column

from customer.serializers import ReviewSerializerPOST
from customer.serializers import ReviewSerializer
from customer.models import Review
from customer.filters import CustomerReviewFilter


class ReviewModelView(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser,)

    def post(self, request, *args, **kwargs):

        serializer = ReviewSerializerPOST(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Successfully added review.',
        }, status=HTTP_201_CREATED)


class ReviewModelViewSet(GenericViewSet, ListModelMixin, ExportData):
    permission_classes = (IsAuthenticated, IsSuperUser,)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = CustomerReviewFilter
    search_fields = ['product__name', 'rating']
    default_fields = [
        'product',
        'comment',
        'rating',
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


