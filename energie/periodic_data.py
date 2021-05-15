from common.datetime_functions import month_list, week_list, day_list
from energie.energie_sets_factory import EnergieSet
from energie.forms import TABLE_PERIOD_WEEKS, TABLE_PERIOD_MONTHS, TABLE_PERIOD_ACTUAL_YEAR, TABLE_PERIOD_DAYS
from energie.models import SmartMeter


class PeriodicData:

    def __init__(self, dt0, dt1, period):
        self.dt0 = dt0
        self.dt1 = dt1
        self.period = period
        if period == TABLE_PERIOD_DAYS:
            self.rr = day_list(dt0, dt1)
        elif period == TABLE_PERIOD_WEEKS:
            self.rr = week_list(dt0, dt1)
        elif period == TABLE_PERIOD_MONTHS:
            self.rr = month_list(dt0, dt1)
        elif period == TABLE_PERIOD_ACTUAL_YEAR:
            pass
        self.sm_list = list()
        self.make_db_query()

    def make_db_query(self):
        for dt_item in list(self.rr):
            qs = SmartMeter.objects.filter(dt__lte=dt_item).order_by('-dt')[:1]
            if qs:
                sm = qs[0]
                self.sm_list.append(sm)

    def get_energyset_list(self):
        energyset_list = list()
        for i in range(1, len(self.sm_list)):
            prod = self.sm_list[i].active_energy_m - self.sm_list[i - 1].active_energy_m
            cons = self.sm_list[i].active_energy_p - self.sm_list[i - 1].active_energy_p
            result = EnergieSet(descriptor=self.period, consumption=cons, production=prod,
                                date_from=self.sm_list[i].dt, date_to=self.sm_list[i].dt)
            energyset_list.append(result)
        return energyset_list
