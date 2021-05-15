from datetime import datetime

from django.db import models
from django_pandas.managers import DataFrameManager

from config.settings.common import TZ


class Wetterdaten(models.Model):
    datumzeit = models.DateTimeField(null=True)
    t = models.FloatField()
    p = models.FloatField()
    h = models.FloatField(null=True)
    dir = models.FloatField(null=True)
    v = models.FloatField(null=True)


    class Meta:
        ordering = ['datumzeit']

    def __repr__(self):
        return "Wetterdaten {}".format(self.datumzeit)

    def __init__(self, *args, **kwargs):
        super(Wetterdaten, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id and self.datumzeit is None:
            self.datumzeit = datetime.now(tz=TZ)
        return super(Wetterdaten, self).save(*args, **kwargs)

    @classmethod
    def data_from_time_period(cls, dt_begin, dt_end):
        qs = Wetterdaten.objects.filter(datumzeit__gte=dt_begin, datumzeit__lt=dt_end)
        if qs and qs.count() > 1000:
            pass
        return qs
