from datetime import datetime, timedelta

import pytest
from django.contrib.auth.models import User
from django.db import connection

from config.settings.common import TZ
from energie.models import SmartMeter


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    assert User.objects.count() == 1


@pytest.fixture
@pytest.mark.django_db(transaction=True)
def create_some_records():
    sm = SmartMeter(dt=datetime(2020, 1, 1, 12, 30, 12, 222222, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 1, 23, 45, 1, tzinfo=TZ), active_energy_p=0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 2, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 2, 12, 45, 2, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 2, 23, 45, 3, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 2, 23, 59, 59, 999999, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 2, 23, 59, 4, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 3, 22, 59, 5, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 4, 8, 45, 6, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 4, 18, 55, 6, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 4, 23, 45, 6, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 5, 23, 45, 6, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 5, 23, 56, 6, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 6, 23, 58, 6, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 7, 23, 50, 59, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    sm = SmartMeter(dt=datetime(2020, 1, 7, 23, 56, 6, tzinfo=TZ), active_energy_p=0.0, active_energy_m=0.0)
    sm.save()
    print("\nfixture: ")
    for item in SmartMeter.objects.all():
        print(item)
    print("end fixture\n")


@pytest.fixture
@pytest.mark.django_db(transaction=True)
def create_some_further_records():
    dt0 = datetime(2020, 1, 1, 23, 59, 59, 999999, tzinfo=TZ)
    alpha = 10
    beta = 40
    aem0 = 1000
    aep0 = 500
    for i in range(0, 101):
        dt = dt0 + timedelta(days=i)
        aep = aep0 + alpha * i
        aem = aem0 + beta * i
        sm = SmartMeter(dt=dt - timedelta(hours=3), active_energy_p=aep, active_energy_m=aem)
        sm.save()
        sm = SmartMeter(dt=dt - timedelta(hours=2), active_energy_p=aep + 1, active_energy_m=aem + 1)
        sm.save()
        sm = SmartMeter(dt=dt - timedelta(hours=1), active_energy_p=aep + 2, active_energy_m=aem + 2)
        sm.save()
        sm = SmartMeter(dt=dt, active_energy_p=aep + 3, active_energy_m=aem + 3)
        sm.save()
        sm = SmartMeter(dt=dt + timedelta(hours=1), active_energy_p=aep + 4, active_energy_m=aem + 4)
        sm.save()
        sm = SmartMeter(dt=dt + timedelta(hours=2), active_energy_p=aep + 5, active_energy_m=aem + 5)
        sm.save()
        sm = SmartMeter(dt=dt + timedelta(hours=3), active_energy_p=aep + 6, active_energy_m=aem + 6)
        sm.save()


@pytest.mark.django_db(transaction=True)
def test_create_list_of_last_day_values(create_some_further_records):
    dt_from = datetime(2020, 1, 3, tzinfo=TZ)
    dt_to = datetime(2020, 1, 6, tzinfo=TZ)
    result = SmartMeter.create_list_of_last_day_values(dt_from, dt_to)
    assert result
    assert 3 == len(result)
    assert datetime(2020, 1, 3, 23, 25, 59, 999999) == result[0][0]


@pytest.mark.django_db(transaction=True)
def test_daily_values(create_some_records):
    dt_begin = datetime(2020, 1, 2, tzinfo=TZ)
    dt_end = datetime(2020, 1, 5, tzinfo=TZ)
    sql = ["SELECT t1.dt, t1.active_energy_p, t1.active_energy_m FROM energie_smartmeter ",
           "t1 LEFT OUTER JOIN energie_smartmeter t2 ON (DATE(t1.dt) = DATE(t2.dt) AND t1.dt < t2.dt) ",
           " WHERE t2.dt IS null;"]
    sql_str = "".join(sql)
    # rows = SmartMeter.objects.raw(sql_str)

    with connection.cursor() as cursor:
        cursor.execute(sql_str)
        rows = cursor.fetchall()

    result_list = list()
    for item in rows:
        dt = item[0]
        dt = dt.replace(tzinfo=TZ)
        if dt_begin <= dt < dt_end:
            result_list.append(item)


@pytest.mark.django_db(transaction=True)
def test_create_list_of_last_day_values(create_some_records):
    dt_begin = datetime(2020, 1, 2, tzinfo=TZ)
    dt_end = datetime(2020, 1, 5, tzinfo=TZ)
    rows = SmartMeter.create_list_of_last_day_values(dt_begin - timedelta(days=1), dt_end)
    # Datum des ersten Records ist das 1 Tag vor dt_begin und die Zeit ist variable
    assert len(rows) == 4
    assert rows[0][0].date() == (dt_begin - timedelta(days=1)).date()
    # Das Datum des letzten Records ist ein Tag vor dt_end
    assert rows[len(rows) - 1][0].date() == (dt_end - timedelta(days=1)).date()
