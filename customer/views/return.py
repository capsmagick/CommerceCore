from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.permissions import IsAuthenticated
from setup.permissions import IsSuperUser

from customer.serializers import ReviewSerializerPOST


