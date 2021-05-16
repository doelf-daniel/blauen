from django.db import models, connection
from django.db.models import AutoField


class SmartMeter(models.Model):
    """
        active_power =      Wirkleistuntg       V*i * cos(phi)
        reactive_power:     Blindleistung       V*i * sin(phin)
        apparent_power:     Scheinleistung      V*i

        Phasendifferenz                         phi

    """
    id = AutoField(primary_key=True)
    dt = models.DateTimeField(null=True, db_index=True)
    active_power_p = models.FloatField(null=False, default=0.0)
    active_power_m = models.FloatField(null=False, default=0.0)
    reactive_power_p = models.FloatField(null=False, default=0.0)
    reactive_power_m = models.FloatField(null=False, default=0.0)
    apparent_power_p = models.FloatField(null=False, default=0.0)
    apparent_power_m = models.FloatField(null=False, default=0.0)
    power_factor = models.FloatField(null=False, default=0.0)
    supply_frequency = models.FloatField(null=False, default=0.0)
    active_energy_p = models.FloatField(null=False, default=0.0)
    active_energy_m = models.FloatField(null=False, default=0.0)
    reactive_energy_p = models.FloatField(null=False, default=0.0)
    reactive_energy_m = models.FloatField(null=False, default=0.0)
    apparent_energy_p = models.FloatField(null=False, default=0.0)
    apparent_energy_m = models.FloatField(null=False, default=0.0)

    def __repr__(self):
        return "SmartMeter {:%d.%m.%Y-%H:%M:%S}".format(self.dt)

    def __str__(self):
        return "SmartMeter: {:%d.%m.%Y-%H:%M:%S}: Active Energiy: p: {:8.3f} m {:8.3f} ". \
            format(self.dt, self.active_energy_p, self.active_energy_m)

    @staticmethod
    def make_str(descriptor, value):
        return "{:30s}  value: {:15.3f} \n".format(descriptor, value)

    def get_data_list(self):
        data_list = list()
        data_list.append(self.make_str('active power +', self.active_power_p))
        data_list.append(self.make_str('active power -', self.active_power_m))
        data_list.append(self.make_str(
            'reactive power +', self.reactive_power_p))
        data_list.append(self.make_str(
            'reactive power -', self.reactive_power_m))
        data_list.append(self.make_str(
            'apparent power +', self.apparent_power_p))
        data_list.append(self.make_str(
            'apparent power -', self.apparent_power_m))

        data_list.append(self.make_str('power factor', self.power_factor))
        data_list.append(self.make_str('frequency', self.supply_frequency))

        data_list.append(self.make_str(
            'active energy +', self.active_energy_p))
        data_list.append(self.make_str(
            'active energy -', self.active_energy_m))
        data_list.append(self.make_str(
            'reactive energy +', self.reactive_energy_p))
        data_list.append(self.make_str(
            'reactive energy -', self.reactive_energy_m))
        data_list.append(self.make_str(
            'apparent energy +', self.apparent_energy_p))
        data_list.append(self.make_str(
            'apparent energy -', self.apparent_energy_m))
        return "".join(data_list)

    def active_energy_difference(self):
        return self.active_energy_m - self.active_energy_p

    @classmethod
    def data_from_time_period(cls, dt_begin, dt_end):
        return SmartMeter.objects.filter(dt__gte=dt_begin, dt__lt=dt_end).order_by('dt')

    @staticmethod
    def create_list_of_last_day_values(dt_from, dt_to):
        # Liefert eine Liste des jeweils letzten Records des Tages (zeitlich gesehen).
        # Also genau ein Record per Tag
        """
        SELECT t1. * FROM smartmeter t1 LEFT OUTER JOIN smartmeter t2
            ON(DATE(t1.dt) = DATE(t2.dt) AND t1.dt < t2.dt) WHERE
                t2.dt IS NULL;

            :return: list
            SELECT t1.dt, t1.active_energy_p, t1.active_energy_m FROM energie_smartmeter
                          t1 LEFT OUTER JOIN energie_smartmeter t2 ON (DATE(t1.dt) = DATE(t2.dt) AND t1.dt < t2.dt)
                            WHERE t2.dt IS null;

        """
        sql_str = "".join(["SELECT t1.dt, t1.active_energy_p, t1.active_energy_m FROM energie_smartmeter ",
                           "t1 LEFT OUTER JOIN energie_smartmeter t2 ON (DATE(t1.dt) = DATE(t2.dt) ",
                           " AND t1.dt < t2.dt) WHERE t2.dt IS null  and t1.dt >= '{}' and t1.dt < '{}';"])
        sql_str = sql_str.format(dt_from, dt_to)

        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            rows = cursor.fetchall()
        return rows

    @staticmethod
    def create_list_of_last_day_records(dt_from, dt_to):
        sql_str = "".join(["SELECT t1 FROM energie_smartmeter ",
                           "t1 LEFT OUTER JOIN energie_smartmeter t2 ON (DATE(t1.dt) = DATE(t2.dt) ",
                           " AND t1.dt < t2.dt) WHERE t2.dt IS null  and t1.dt >= '{}' and t1.dt < '{}';"])
        sql_str = sql_str.format(dt_from, dt_to)

        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            rows = cursor.fetchall()
        return rows


class EnergieSet:
    def __init__(self, descriptor='undefined', consumption=0.0, production=0.0,
                 date_from=None, date_to=None):
        self.descriptor = descriptor
        self.consumption = consumption
        self.production = production
        self.date_from = date_from
        self.date_to = date_to

    def __str__(self):
        return "EnergieSet: {}, consumption : {:.2f}, production: {:.2f}". \
            format(self.descriptor, self.consumption, self.production)

    def difference(self):
        if self.production is not None and self.consumption is not None:
            return self.production - self.consumption
        else:
            raise ValueError("One or more values are undefined!")
