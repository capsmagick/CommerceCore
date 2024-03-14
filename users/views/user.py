from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from rest_framework.permissions import AllowAny

from setup.views import BaseModelViewSet
from users.models import User
from users.serializers import StoreManagerModelSerializer

from .utils import get_userdata


@method_decorator(ensure_csrf_cookie, name='dispatch')
class Me(APIView):
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
    default_fields = [
        'username', 'first_name', 'last_name',
        'email', 'mobile_number'
    ]
    search_fields = [
        'username', 'first_name', 'email', 'mobile_number'
    ]


