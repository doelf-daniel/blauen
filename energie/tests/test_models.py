from datetime import datetime, timedelta

from dateutil import tz
from django.test import TestCase

from energie.models import SmartMeter


class SmartMeterModelTest(TestCase):

    def setUp(self):
        self.timezone = tz.gettz('Europe/Zurich')
        now = datetime.now(tz=self.timezone)
        # now = datetime.now()
        SmartMeter.objects.create(dt=now)

    def test_query(self):
        qs = SmartMeter.objects.all()
        print(qs.first())
        self.assertEqual(1, qs.count())

    def test_query_empty_db(self):
        SmartMeter.objects.all().delete()
        qs = SmartMeter.objects.all()
        self.assertEqual(0, qs.count())

    def test_data_from_time_period(self):
        dt_end = datetime.now(tz=self.timezone)
        dt_begin = dt_end - timedelta(days=2)
        qs = SmartMeter.data_from_time_period(dt_begin, dt_end)
        self.assertEqual(1, qs.count())
        SmartMeter.objects.all().delete()
        qs = SmartMeter.data_from_time_period(dt_begin, dt_end)
        self.assertEqual(0, qs.count())
