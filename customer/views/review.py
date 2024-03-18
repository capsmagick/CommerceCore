from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin

from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.permissions import IsAuthenticated
from setup.permissions import IsSuperUser

from customer.serializers import ReviewSerializerPOST


class ReviewModelView(APIView):
    permission_classes = (IsAuthenticated, IsSuperUser,)

    def post(self, request, *args, **kwargs):

        serializer = ReviewSerializerPOST(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Successfully added review.',
        }, status=HTTP_201_CREATED)


