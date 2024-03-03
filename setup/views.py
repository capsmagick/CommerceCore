from rest_framework import status
from rest_framework import mixins
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .utils import generate_column


class BaseModelViewSet(
    GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin
):
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    queryset = None
    serializer_class = None
    default_fields = []
    include_actions = True
    multiple_lookup_fields = []

    @action(detail=False, methods=['POST'])
    def create_record(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_db_action(serializer)
        return Response(
            {
                'data': serializer.data,
                'message': 'Successfully Created'
            },
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['PUT'])
    def update_record(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_db_action(serializer)
        return Response(
            {
                'data': serializer.data,
                'message': 'Successfully Updated'
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['DELETE'])
    def delete_record(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_delete(instance)
        return Response(
            {
                'message': 'Successfully Deleted'
            },
            status=status.HTTP_200_OK
        )

    def perform_db_action(self, serializer):
        serializer.save()

    def perform_delete(self, instance):
        instance.delete()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        try:
            response.data['columns'] = generate_column(
                self.queryset.model, actions=self.include_actions,
                default_fields=self.default_fields
            )
        except Exception as e:
            print('Exception occurred while generating the columns : ', e)
        return response
