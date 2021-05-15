from datetime import datetime

# Create your tests here.
import pytest

from config.settings.common import TZ
from energie.models import SmartMeter


@pytest.fixture
@pytest.mark.django_db(transaction=True)
def create_some_records():
    sm = SmartMeter(dt=datetime(2020, 1, 1, 12, 30, 12, 222222, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 1, 23, 45, 1, 0, tzinfo=TZ), active_energy_p=0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 2, 0, 0, 0, 0, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 2, 12, 45, 2, 0, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 2, 23, 45, 3, 0, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 2, 23, 59, 59, 999999, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 2, 23, 59, 4, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 3, 22, 59, 5, 0, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 4, 8, 45, 6, 0, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 4, 18, 55, 6, 0, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 4, 23, 45, 6, 0, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 5, 23, 45, 6, 0, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 5, 23, 56, 6, 0, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 6, 23, 58, 6, 0, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 7, 23, 50, 59, 0, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 7, 23, 56, 6, 0, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    print("\nfixture: ")
    for item in SmartMeter.objects.all():
        print(item)
    print("end fixture\n")
