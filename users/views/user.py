from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny, IsAuthenticated

from setup.views import BaseModelViewSet
from setup.permissions import IsSuperUser
from users.models import User
from users.serializers import StoreManagerModelSerializer
from users.serializers import UserDataModelSerializer
from users.serializers import UserModelSerializerGET

from .utils import get_userdata


@method_decorator(ensure_csrf_cookie, name='dispatch')
class Me(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        """
            Refresh session API

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """

        user = request.user

        if user.is_authenticated:
            response = Response({
                'loggedIn': True,
                'user': get_userdata(user)
            }, status=status.HTTP_200_OK)
            return response

        else:
            return Response({
                'loggedIn': False,
            }, status=status.HTTP_200_OK)


class CustomerMe(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        user = request.user

        if user.is_authenticated:
            response = Response({
                'loggedIn': True,
                'user': get_userdata(user)
            }, status=status.HTTP_200_OK)
            return response

        else:
            return Response({
                'loggedIn': False,
            }, status=status.HTTP_200_OK)


class StoreManagerViewSet(BaseModelViewSet):
    queryset = User.objects.filter(deleted=False, store_manager=True)
    serializer_class = StoreManagerModelSerializer
    retrieve_serializer_class = UserModelSerializerGET
    default_fields = [
        'username', 'first_name', 'last_name',
        'email', 'mobile_number'
    ]
    search_fields = [
        'username', 'first_name', 'email', 'mobile_number'
    ]


class CustomerViewSet(GenericViewSet, ListModelMixin):
    permission_classes = (IsAuthenticated, IsSuperUser)
    queryset = User.objects.filter(deleted=False, is_customer=True)
    serializer_class = UserDataModelSerializer



