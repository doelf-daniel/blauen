from datetime import datetime

from common.datetime_functions import begin_of_week_with_date, begin_of_month_with_date
from common.datetime_functions import diff_month, list_month_begin, month_list, week_list
from config.settings.common import TZ


def test_begin_actual_week_0():
    dt_begin = datetime(2020, 5, 11, 0, tzinfo=TZ)
    res = begin_of_week_with_date(dt_begin)
    assert res == dt_begin


def test_begin_actual_week_1():
    dt_begin = datetime(2020, 5, 14, 0, tzinfo=TZ)
    res = begin_of_week_with_date(dt_begin)
    assert datetime(2020, 5, 11, 0, tzinfo=TZ) == res


def test_begin_actual_week_7():
    dt_begin = datetime(2020, 5, 17, 0, tzinfo=TZ)
    res = begin_of_week_with_date(dt_begin)
    assert datetime(2020, 5, 11, 0, tzinfo=TZ) == res


def test_begin_actual_month_0():
    dt_begin = datetime(2020, 5, 17, 0, tzinfo=TZ)
    res = begin_of_month_with_date(dt_begin)
    assert datetime(2020, 5, 1, tzinfo=TZ) == res


def test_begin_actual_month_1():
    dt_begin = datetime(2020, 5, 1, 0, tzinfo=TZ)
    res = begin_of_month_with_date(dt_begin)
    assert datetime(2020, 5, 1, tzinfo=TZ) == res


def test_begin_actual_month_2():
    dt_begin = datetime(2020, 5, 31, 0, tzinfo=TZ)
    res = begin_of_month_with_date(dt_begin)
    assert datetime(2020, 5, 1, tzinfo=TZ) == res


def test_begin_month_actual():
    dt_ref = datetime(2020, 5, 17, 0, tzinfo=TZ)
    dt0 = begin_of_month_with_date(dt_ref)
    assert dt0 == datetime(2020, 5, 1, tzinfo=TZ)


def test_diff_month():
    assert diff_month(datetime(2010, 10, 1), datetime(2010, 10, 1)) == 0
    assert diff_month(datetime(2010, 10, 1), datetime(2010, 9, 1)) == 1
    assert diff_month(datetime(2010, 10, 2), datetime(2010, 9, 1)) == 1
    assert diff_month(datetime(2010, 10, 31), datetime(2010, 9, 1)) == 1
    assert diff_month(datetime(2010, 10, 1), datetime(2009, 10, 1)) == 12
    assert diff_month(datetime(2010, 10, 1), datetime(2009, 11, 1)) == 11
    assert diff_month(datetime(2010, 10, 1), datetime(2009, 8, 1)) == 14


def test_list_month_begin_0():
    dt = datetime(2019, 2, 1)
    no = 0
    res = list_month_begin(dt, no)
    assert 0 == len(res)


def test_list_month_begin_1():
    dt = datetime(2019, 2, 1)
    no = 1
    res = list_month_begin(dt, no)
    assert res
    assert 1 == len(res)


def test_list_month_begin_5():
    dt = datetime(2019, 2, 1)
    no = 5
    res = list_month_begin(dt, no)
    assert res
    assert 5 == len(res)


def test_list_month_begin_30():
    dt = datetime(2019, 2, 1)
    no = 30
    res = list_month_begin(dt, no)
    assert res
    assert 30 == len(res)


def test_month_list_1():
    dt_start = datetime(2020, 2, 5, tzinfo=TZ)
    dt_end = datetime(2020, 7, 15, tzinfo=TZ)
    rr = month_list(dt_start=dt_start, dt_end=dt_end)
    for item in list(rr):
        print(item)


def test_month_list_2():
    dt_start = datetime(2019, 3, 25, tzinfo=TZ)
    dt_end = datetime(2020, 7, 15, tzinfo=TZ)
    rr = month_list(dt_start=dt_start, dt_end=dt_end)
    for item in list(rr):
        print(item)


def test_week_list_1():
    dt_start = datetime(2020, 2, 5, tzinfo=TZ)
    dt_end = datetime(2020, 4, 15, tzinfo=TZ)
    rr = week_list(dt_start=dt_start, dt_end=dt_end)
    for item in list(rr):
        print(item)
