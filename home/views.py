from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from setup.permissions import IsSuperUser

from users.models import User
from orders.models import Order


class DashboardAPIView(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser,)

    def get(self, request, *args, **kwargs):
        pass


