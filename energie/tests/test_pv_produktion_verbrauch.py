from datetime import date
from unittest.case import TestCase

from energie.forms import TABLE_PERIOD_WEEKS
from energie.views import PvProduktionVerbrauch


class TestPvProduktionVerbrauch(TestCase):

    def test_process_filter_data_1(self):
        obj = PvProduktionVerbrauch()
        dt0 = date(2020, 4, 1)
        dt1 = date(2020, 4, 11)
        period = TABLE_PERIOD_WEEKS
        dt01, dt11 = obj.process_filter_data(dt0, dt1, period)
        self.assertEqual(dt01, date(2020, 3, 30))
        self.assertEqual(dt11, date(2020, 4, 6))

    def test_process_filter_data_2(self):
        obj = PvProduktionVerbrauch()
        dt0 = date(2020, 4, 1)
        dt1 = date(2020, 4, 11)
        period = TABLE_PERIOD_WEEKS
        dt01, dt11 = obj.process_filter_data(dt0, dt1, period)
        self.assertEqual(dt01, date(2020, 3, 30))
        self.assertEqual(dt11, date(2020, 4, 6))

    def test_process_filter_data_3(self):
        obj = PvProduktionVerbrauch()
        dt0 = date(2020, 5, 4)
        dt1 = date(2020, 5, 10)
        period = TABLE_PERIOD_WEEKS
        dt01, dt11 = obj.process_filter_data(dt0, dt1, period)
        self.assertEqual(dt01, date(2020, 4, 27))
        self.assertEqual(dt11, date(2020, 5, 4))
