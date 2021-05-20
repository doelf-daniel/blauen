from datetime import datetime, timedelta

from dateutil.rrule import rrule, MONTHLY, WEEKLY, DAILY

from config.settings.common import TZ


def begin_of_week_with_date(dt_begin):
    return dt_begin - timedelta(days=dt_begin.weekday())


def begin_month_before(dt_ref):
    month = dt_ref.month
    if month == 1:
        dt = datetime(dt_ref.year - 1, 12, 1, tzinfo=TZ)
    else:
        dt = datetime(dt_ref.year, dt_ref.month, 1, tzinfo=TZ)
    return dt


def begin_of_month_with_date(dt_ref):
    return dt_ref.replace(day=1)


def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def list_month_begin(dt, no):
    dt_list = list()
    if no > 0:
        month = dt.month
        year = dt.year
        day = dt.day
        dt_list.append(dt)
        for i in range(1, no):
            month += 1
            if month > 12:
                month = 1
                year += 1
            dtx = datetime(year, month, day, tzinfo=TZ)
            dt_list.append(dtx)
    return dt_list


def month_list(dt_start, dt_end):
    rr = rrule(freq=MONTHLY, dtstart=dt_start, until=dt_end, bymonthday=1)
    return rr


def week_list(dt_start, dt_end):
    rr = rrule(freq=WEEKLY, dtstart=dt_start, until=dt_end, byweekday=0)
    return rr


def day_list(dt_start, dt_end):
    rr = rrule(freq=DAILY, dtstart=dt_start, until=dt_end)
    return rr
