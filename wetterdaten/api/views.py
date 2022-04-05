import logging

from rest_framework import permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from wetterdaten.api.serializers import WetterdatenSerializer
from wetterdaten.models import Wetterdaten

logger = logging.getLogger(__name__)


#
# class WetterdatenViewSet(ModelViewSet):
#     authentication_classes = []
#     permission_classes = []
#     queryset = Wetterdaten.objects.all().order_by('-id')[:20]
#     serializer_class = WetterdatenSerializer

class WetterDatenList(APIView):
    """
    List all SmartMeter objects, or create a new SmartMeter object.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        snippets = Wetterdaten.objects.all().order_by('-datumzeit')[:10]
        serializer = WetterdatenSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WetterdatenSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except AssertionError:
                logger.error("assertion error on save", exc_info=True)
        else:
            logger.error("Serializer got invalid data: {}".format(serializer.data), exc_info=True)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
