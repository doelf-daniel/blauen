from datetime import date
from datetime import datetime, timedelta

import pytest

from blauen.settings.common import TZ
from energie.energie_sets_factory import create_energy_set_per_day, EnergieSet, create_energy_set_per_week
from energie.models import SmartMeter


def test_energie_set_0():
    result = EnergieSet()
    assert result is not None
    assert result.consumption == 0.0
    assert result.production == 0.0
    assert result.difference() == 0.0
    assert result.descriptor == 'undefined'
    assert result.date_from is None
    assert result.date_to is None


def test_energie_set_1():
    dt = date.today()
    cons = 22.22
    prod = 55.55
    result = EnergieSet(descriptor='so en Saich', consumption=cons, production=prod,
                        date_from=dt, date_to=dt)
    assert result is not None
    assert result.consumption == cons
    assert result.production == prod
    assert result.difference() == prod - cons
    assert result.descriptor == 'so en Saich'
    assert result.date_from == dt
    assert result.date_to == dt


@pytest.fixture
@pytest.mark.django_db(transaction=True)
def create_some_further_records():
    a1 = 1000
    b1 = 2000
    dt0 = datetime(2020, 4, 3, tzinfo=TZ)
    for i in range(0, 40):
        a1 += i
        b1 = b1 + 10 + i

        dt = dt0 + timedelta(days=i)
        sm = SmartMeter(dt=dt + timedelta(hours=1), active_energy_p=a1 + 1, active_energy_m=b1 + 1)
        sm.save()
        sm = SmartMeter(dt=dt + timedelta(hours=12), active_energy_p=a1 + 2, active_energy_m=b1 + 2)
        sm.save()
        sm = SmartMeter(dt=dt + timedelta(hours=23), active_energy_p=a1 + 3, active_energy_m=b1 + 3)
        sm.save()


@pytest.mark.django_db(transaction=True)
def test_create_energy_set_per_day_0():
    dt = datetime(2020, 4, 1)
    result = create_energy_set_per_day(dt)
    assert result
    assert 0.0 == result.production
    assert 0.0 == result.consumption


@pytest.mark.django_db(transaction=True)
def test_create_energy_set_per_day_1(create_some_further_records):
    dt = datetime(2020, 4, 20, tzinfo=TZ)
    # data = list(SmartMeter.objects.all())
    result = create_energy_set_per_week(dt, 1)
    assert result.consumption == 91
    assert result.production == 161
    assert result.descriptor == 'Wochendaten'


@pytest.mark.django_db(transaction=True)
def test_create_energy_set_per_day_2(create_some_further_records):
    dt = datetime(2020, 4, 26, tzinfo=TZ)
    result = create_energy_set_per_week(dt, 1)
    assert result.consumption == 91
    assert result.production == 161
    assert result.descriptor == 'Wochendaten'


@pytest.mark.django_db(transaction=True)
def test_create_energy_set_per_day_3(create_some_further_records):
    dt = datetime(2020, 4, 26, tzinfo=TZ)
    try:
        create_energy_set_per_week(dt, 0)
        assert False
    except ValueError:
        assert True
