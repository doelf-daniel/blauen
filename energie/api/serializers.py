import logging

from rest_framework import serializers

from energie.models import SmartMeter

logger = logging.getLogger(__name__)


class SmartMeterDatenSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmartMeter
        fields = ('dt', 'active_power_p', 'active_power_m',
                  'reactive_power_p', 'reactive_power_m',
                  'apparent_power_p', 'apparent_power_m',
                  'power_factor', 'supply_frequency',
                  'active_energy_p', 'active_energy_m',
                  'reactive_energy_p', 'reactive_energy_m',
                  'apparent_energy_p', 'apparent_energy_m')
