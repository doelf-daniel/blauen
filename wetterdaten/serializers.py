from rest_framework import serializers

from .models import Wetterdaten


class WetterdatenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wetterdaten
        fields = ('id', 'datumzeit', 't', 'p', 'h', 'v', 'dir')
