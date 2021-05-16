import logging

import matplotlib.pyplot as plt
from django.utils import timezone
from django_pandas.io import read_frame
from matplotlib.dates import (ConciseDateFormatter, AutoDateLocator)
from pandas.plotting import register_matplotlib_converters

from .models import Wetterdaten

register_matplotlib_converters()

logger = logging.getLogger(__name__)


def create_dataframe(dt_begin, dt_end):
    query_set = Wetterdaten.data_from_time_period(dt_begin, dt_end)
    # dataframe = query_set.to_dataframe(['t', 'p', 'h'], index='datumzeit')
    dataframe = read_frame(query_set)

    # create datetime index passing the datetime series

    # tz_convert  --> timezone
    # todo  dataframe = dataframe.tz_convert("Europe/Zurich")
    try:
        resample = dataframe.resample('H').mean()
    except Exception as ex:
        logger.warning("resample failed!\n{}".format(ex))
        resample = dataframe
    return resample


def temperature_chart(dt_begin, dt_end):
    dt_begin = dt_begin.astimezone(tz=timezone.utc)
    dt_end = dt_end.astimezone(tz=timezone.utc)
    query_set = Wetterdaten.objects.filter(datumzeit__gte=dt_begin, datumzeit__lt=dt_end).order_by('datumzeit')
    if query_set.count() > 3:
        x = list()
        y1 = list()
        for item in query_set:
            dt = item.datumzeit.astimezone(tz=timezone.utc)
            x.append(dt)
            y1.append(item.t)

        fig, ax1 = plt.subplots(1, 1)
        fig.set_size_inches(12.0, 8.0)
        plt.plot(x, y1, linewidth=2, linestyle='-', markersize=1)

        ax1.set_xlabel('Zeit')
        ax1.set_ylabel('Temperatur [°C]')
        plt.grid(True)
        ax1.set_ylim(-10.0, 35.0)
        ax1.set_title("Temperaturverlauf Laufenburg")
        ax1.minorticks_on()
        ax1.tick_params(which='minor', length=3, width=1, direction='in')
        ax1.tick_params(which='major', length=10, width=1, direction='out')
        # ax1.xaxis.set_major_formatter(plt.FuncFormatter(format_func))

        locator = AutoDateLocator()
        formatter = ConciseDateFormatter(locator)
        formatter.formats[0] = '%Y.%m.%d'
        formatter.formats[2] = '%d-%H.%M'
        ax1.xaxis.set_major_formatter(formatter)
        ax1.xaxis.set_major_formatter(formatter)

        for label in ax1.get_xticklabels():
            label.set_rotation(40)
            label.set_horizontalalignment('right')
        return fig
    else:
        return None


def pressure_chart(dt_begin, dt_end):
    dt_begin = dt_begin.astimezone(tz=timezone.utc)
    dt_end = dt_end.astimezone(tz=timezone.utc)
    query_set = Wetterdaten.objects.filter(datumzeit__gte=dt_begin, datumzeit__lt=dt_end).order_by('datumzeit')
    if query_set.count() > 3:
        x = list()
        y1 = list()
        for item in query_set:
            dt = item.datumzeit.astimezone(tz=timezone.utc)
            x.append(dt)
            y1.append(item.p)

        fig, ax1 = plt.subplots(1, 1)
        fig.set_size_inches(12.0, 8.0)
        plt.plot(x, y1, linewidth=2, linestyle='-', markersize=1)

        ax1.set_xlabel('Zeit')
        ax1.set_ylabel('Luftdruck [mBar')
        plt.grid(True)
        ax1.set_ylim(800, 1100)
        ax1.set_title("Luftdruck Laufenburg")
        ax1.minorticks_on()
        ax1.tick_params(which='minor', length=3, width=1, direction='in')
        ax1.tick_params(which='major', length=10, width=1, direction='out')
        # ax1.xaxis.set_major_formatter(plt.FuncFormatter(format_func))

        locator = AutoDateLocator()
        formatter = ConciseDateFormatter(locator)
        formatter.formats[0] = '%Y.%m.%d'
        formatter.formats[2] = '%d-%H.%M'
        ax1.xaxis.set_major_formatter(formatter)
        ax1.xaxis.set_major_formatter(formatter)

        for label in ax1.get_xticklabels():
            label.set_rotation(40)
            label.set_horizontalalignment('right')
        return fig
    else:
        return None
