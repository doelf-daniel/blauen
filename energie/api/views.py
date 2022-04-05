import logging

from rest_framework import status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from energie.api.serializers import SmartMeterDatenSerializer
from energie.models import SmartMeter

logger = logging.getLogger(__name__)


class SmartMeterList(APIView):
    """
    List all SmartMeter objects, or create a new SmartMeter object.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        snippets = SmartMeter.objects.all().order_by('-dt')[:10]
        serializer = SmartMeterDatenSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SmartMeterDatenSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except AssertionError:
                logger.error("assertion error on save", exc_info=True)
        else:
            logger.error("Serializer got invalid data: {}".format(serializer.data), exc_info=True)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
