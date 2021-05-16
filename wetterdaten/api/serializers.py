import logging

from rest_framework import serializers

from wetterdaten.models import Wetterdaten

logger = logging.getLogger(__name__)


class WetterdatenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wetterdaten
        fields = ('id', 'datumzeit', 't', 'p', 'h', 'dir', 'v')
