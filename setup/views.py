from rest_framework import status
from rest_framework import mixins
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from setup.permissions import IsSuperUser
from setup.utils import generate_column


class BaseModelViewSet(
    GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin
):
    """
        BaseModelViewSet
        This class is a base class for creating Normal CRUD API for all models.
    """
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    permission_classes = (IsAuthenticated, IsSuperUser,)
    queryset = None
    serializer_class = None
    retrieve_serializer_class = None
    default_fields = []
    include_actions = True
    multiple_lookup_fields = []
    search_fields = []

    def get_serializer_class(self):
        """
            Return the class to use for the serializer.
            Defaults to using `self.serializer_class or self.retrieve_serializer_class`.

            self.retrieve_serializer_class : Used to list function for data serializing
            self.serializer_class : Used to actions like CREATE, UPDATE

            You may want to override this if you need to provide different
            serializations depending on the incoming request.

            (Eg. admins get full serialization, others get basic serialization)
        """
        if self.action == 'list' and self.retrieve_serializer_class:
            return self.retrieve_serializer_class
        return self.serializer_class

    @action(detail=False, methods=['POST'])
    def create_record(self, request, *args, **kwargs):
        """
            Create a new record

            Parameters:
            request (HttpRequest): The HTTP request object containing model data.
            any: other data according to the serializer class

            Returns:
            Response: A DRF Response object with the creation status.
        """
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
        """
            Update an existing record

            Parameters:
            request (HttpRequest): The HTTP request object containing model data.

            Returns:
            Response: A DRF Response object with the update status.
        """
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
        """
            Delete an existing record

            Parameters:
            request (HttpRequest): The HTTP request object containing model data.
            pk (int): The primary key of the model to be deleted.

            Returns:
            Response: A DRF Response object indicating success or failure.
        """
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
