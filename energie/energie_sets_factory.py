from datetime import date, timedelta, datetime

from django.utils import timezone

from config.settings.common import TZ
from energie.forms import TABLE_PERIOD_DAYS, TABLE_PERIOD_WEEKS, TABLE_PERIOD_ACTUAL_YEAR
from energie.models import SmartMeter, EnergieSet


def create_energy_set_per_day(dt: datetime):
    """
    Erstellt die Tagesdaten des Vortags (bezüglich Referenzdatum)
    :param dt:  Referenzdatum
    :return:    Objekt der Klasse EnrgieSet mit den Tagesdaten
    """
    if isinstance(dt, date):
        dt = datetime(dt.year, dt.month, dt.day, 0, tzinfo=TZ)
    dt_begin = dt - timedelta(days=1)
    dt_end = dt
    return create_energy_cons_prod_period(dt_begin, dt_end)


def create_energy_cons_prod_period(dt_begin: datetime, dt_end: datetime) -> EnergieSet:
    """
    Ermittelt den Verbrauch und die Produktion im Bereich gegeben durch die Parameter
    dt_from und dt_to

    :param dt_begin:  Beginn der Periode
    :param dt_end:    Ende der Persiode, exklusiv
    :return:          Objekt der Klasse EnrgieSet mit den Produktions- und Verbrauchsdaten
    """
    dt_from = dt_begin.replace(hour=0, minute=0, second=0, microsecond=0)
    dt_to = dt_end.replace(hour=0, minute=0, second=0, microsecond=0)
    dt_from = dt_from.astimezone(tz=timezone.utc)
    dt_to = dt_to.astimezone(tz=timezone.utc)
    rows = SmartMeter.objects.filter(dt__lte=dt_from).order_by('-dt')[:1]
    sm1 = None
    sm2 = None
    if rows:
        sm1 = rows[0]
    rows = SmartMeter.objects.filter(dt__lte=dt_to).order_by('-dt')[:1]
    if rows:
        sm2 = rows[0]
    if sm1 and sm2:
        cons = sm2.active_energy_p - sm1.active_energy_p
        prod = sm2.active_energy_m - sm1.active_energy_m
        result = EnergieSet(descriptor=TABLE_PERIOD_DAYS, consumption=cons, production=prod,
                            date_from=dt_from, date_to=dt_to)
    else:
        result = EnergieSet(descriptor=TABLE_PERIOD_DAYS, consumption=0.0, production=0.0,
                            date_from=dt_from, date_to=dt_to)
    return result


def create_energy_set_per_week(actual_date, week=1):
    """

    :param actual_date:  Referenzdatum in der Referenzwoche
    :param week:         Anzahl Wochen zurück von der Referenzwoche aus gesehen
    :return:             EnergieSet Objekt mit den entsprechenden Daten
    """
    if isinstance(actual_date, date):
        actual_date = datetime(actual_date.year, actual_date.month, actual_date.day, 0, 0, 0, tzinfo=TZ)
    begin_actual_week = actual_date - timedelta(days=actual_date.weekday())
    date_to = begin_actual_week - timedelta(7 * (week - 1))
    date_from = begin_actual_week - timedelta(days=7 * week)
    es = create_energy_cons_prod_period(date_from, date_to)
    es.descriptor = TABLE_PERIOD_WEEKS
    return es


def create_energy_set_actual_year(actual_date: datetime) -> EnergieSet:
    if isinstance(actual_date, date):
        actual_date = datetime(actual_date.year, actual_date.month, actual_date.day, 0, 0, 0, tzinfo=TZ)
    dt_begin = datetime(actual_date.year, 1, 1, 0, 0, 0, tzinfo=TZ)
    qs0 = SmartMeter.objects.filter(dt__gte=dt_begin).order_by('dt')[:1]
    if len(qs0) > 0:
        smart_meter_0 = qs0[0]
        qs1 = SmartMeter.objects.filter(dt__lte=actual_date).order_by('-dt')[:1]
        smart_meter_1 = qs1[0]
        cons = smart_meter_1.active_energy_m - smart_meter_0.active_energy_m
        prod = smart_meter_1.active_energy_p - smart_meter_0.active_energy_p
        result = EnergieSet(descriptor=TABLE_PERIOD_ACTUAL_YEAR, consumption=cons, production=prod,
                            date_from=dt_begin, date_to=actual_date)
    else:
        result = None
    return result