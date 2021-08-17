import matplotlib.pyplot as plt
from django.utils import timezone
from matplotlib.dates import AutoDateLocator, ConciseDateFormatter

from energie.models import SmartMeter


def create_power_chart(dt_begin, dt_end):
    dt_begin = dt_begin.astimezone(tz=timezone.utc)
    dt_end = dt_end.astimezone(tz=timezone.utc)
    query_set = SmartMeter.objects.filter(dt__gte=dt_begin, dt__lt=dt_end).order_by('dt')
    if query_set.count() > 3:
        x = list()
        y1 = list()
        y2 = list()
        for item in query_set:
            dt = item.dt.astimezone(tz=timezone.utc)
            x.append(dt)
            y1.append(item.active_power_p)
            y2.append(item.active_power_m)

        fig, ax1 = plt.subplots()
        fig.set_size_inches(12.0, 8.0)
        plt.plot(x, y1, linewidth=2, linestyle='-', markersize=1)
        plt.plot(x, y2, linewidth=2, linestyle='-', markersize=1)
        ax1.set_xlabel('Zeit')
        ax1.set_ylabel('Leistung [kW')
        plt.grid(True)
        ax1.set_ylim(-0.5, 10.0)
        ax1.set_title("Produktion/Verbrauch")

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
