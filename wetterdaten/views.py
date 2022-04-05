import base64
import logging
import os
from datetime import datetime, timedelta, date
from io import BytesIO

import matplotlib.pyplot as plt
import pytz
from django.conf import settings
from django.utils import timezone
from django.views.generic import TemplateView, DetailView
from matplotlib.dates import AutoDateLocator, ConciseDateFormatter
from pandas.plotting import register_matplotlib_converters

from common.models import (DAUER_WOCHE)
from config.settings.common import TZ
from .forms import SelectForm, SelectDateForm
from .models import Wetterdaten

register_matplotlib_converters()

logger = logging.getLogger(__name__)


def path4chart_factory(file_name):
    chart_path = os.path.join(settings.PROJ_DIR, 'static', 'temp', file_name)
    return chart_path


def create_image_base64(fig):
    """
        Create Base64-String eines Bildes (fig)
    """
    buf = BytesIO()
    fig.savefig(buf, format='png')
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()
    return image_base64


class WetterdatenChartsView(TemplateView):
    template_name = 'wetterdaten/ptchart.html'
    list_t = None
    list_p = None
    list_h = None
    list_dt = None

    def create_image_update_context(self, fig, context):
        if fig is not None:
            try:
                image_base64 = create_image_base64(fig)
                context.update({'image_base64_1': image_base64})
                context.update({'data': 'has_data'})
            except Exception as ex:
                logger.warning("Bilddatei nicht gefunden!", ex)
        else:
            context.update({'data': 'has no data'})

    def daten_array_wetter_diagramm_erstellen(self, dt_begin, dt_end):
        if type(dt_begin) == date:
            dt_begin = datetime(year=dt_begin.year, month=dt_begin.month, day=dt_begin.day)
        if type(dt_end) == date:
            dt_end = datetime(year=dt_end.year, month=dt_end.month, day=dt_end.day)
        # convert local datetime to utc
        dt_begin_utc = dt_begin.astimezone(tz=timezone.utc)
        dt_end_utc = dt_end.astimezone(tz=timezone.utc)
        self.list_t = []
        self.list_p = []
        self.list_h = []
        self.list_dt = []
        query_set = Wetterdaten.data_from_time_period(dt_begin_utc, dt_end_utc)

        for item in query_set:
            self.list_t.append(item.t)
            self.list_p.append(item.p)
            self.list_h.append(item.h)
            item.datumzeit.astimezone(tz=pytz.timezone("Europe/Zurich"))
            self.list_dt.append(item.datumzeit)

    @classmethod
    def create_filter_dict(cls, beginn, ende, dauer):
        filter_dict = dict()
        filter_dict['dauer'] = dauer
        filter_dict['beginn'] = beginn
        filter_dict['ende'] = ende
        return filter_dict

    def get(self, request, *args, **kwargs):
        dt_end = datetime.now(tz=TZ)
        dt_begin = dt_end - timedelta(days=7)
        dt_begin = dt_begin.replace(hour=0, minute=0, second=0, microsecond=0)
        self.daten_array_wetter_diagramm_erstellen(dt_begin, dt_end)
        filter_dict = self.create_filter_dict(dt_begin, dt_end, DAUER_WOCHE)

        fig = self.make_plot(dt_begin, dt_end)
        context = super(WetterdatenChartsView, self).get_context_data(**kwargs)
        form = SelectForm(initial=filter_dict)
        context.update({'form': form})
        self.create_image_update_context(fig, context)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = SelectForm(data=request.POST)
        context = super().get_context_data()
        if form.is_valid():
            # make query
            dt_begin = form.cleaned_data['beginn']
            dt_end = form.cleaned_data['ende']
            dauer = form.cleaned_data['dauer']
            # neue Werte aufgrund der Auswahl
            filter_dict = self.create_filter_dict(dt_begin, dt_end, dauer)
            form = SelectForm(initial=filter_dict)
            self.daten_array_wetter_diagramm_erstellen(dt_begin, dt_end)
            fig = self.make_plot(dt_begin, dt_end)
            context = super(WetterdatenChartsView, self).get_context_data(**kwargs)
            self.create_image_update_context(fig, context)
        else:
            logger.warning("invalid form")

        context.update({'form': form})
        return self.render_to_response(context)

    def make_plot(self, dt_begin, dt_end):
        if self.list_dt and len(self.list_dt) > 0:
            x = self.list_dt
            y1 = self.list_t

            fig, ax1 = plt.subplots(1, 1)
            fig.set_size_inches(12.0, 8.0)
            plt.plot(x, y1, linewidth=2, linestyle='-', color="blue", markersize=1)
            ax1.set_xlabel('Zeit')
            ax1.set_ylabel('Temperatur [°C]', color="blue", fontsize=16)
            plt.grid(True)
            ax1.set_ylim(-10.0, 40.0)
            ax1.set_title("Temperaturverlauf Laufenburg")
            ax1.minorticks_on()
            ax1.tick_params(which='minor', length=3, width=1, direction='in')
            ax1.tick_params(which='major', length=10, width=1, direction='out')
            # ax1.xaxis.set_major_formatter(plt.FuncFormatter(format_func))
            # ax2 = ax1.twinx()
            # ax2.plot(x, self.list_p, linewidth=2, linestyle='-', color="red", markersize=1)
            # ax2.set_ylim(850.0, 1050.0)
            # ax2.set_ylabel('Luftdruck [mBar]', color="red", fontsize=16)

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


class WetterdatenAktuellView(DetailView):
    template_name = "wetterdaten/details.html"

    def get(self, request, *args, **kwargs):
        count = Wetterdaten.objects.count()
        if count > 0:
            latest_record = Wetterdaten.objects.latest('datumzeit')
            context = {'object': latest_record}
        else:
            context = {'no_data': True}
        return self.render_to_response(context)


class WetterDatenListeTag(TemplateView):
    template_name = 'wetterdaten/wetterdatenlistetag.html'
    title = 'Wetterdaten eines Tages'

    @classmethod
    def create_filter_dict(cls, begin):
        filter_dict = dict()
        filter_dict['begin'] = begin
        return filter_dict

    def get(self, request, *args, **kwargs):
        # Daten des aktuellen Tages
        dt_end = datetime.now(tz=TZ)
        dt_begin = datetime(dt_end.year, dt_end.month,
                            dt_end.day, 0, 0, 0, 0, tzinfo=TZ)
        dt_begin_utc = dt_begin.astimezone(tz=timezone.utc)
        dt_end_utc = dt_end.astimezone(tz=timezone.utc)
        form = SelectDateForm(initial={'begin': dt_end})
        context = super().get_context_data(**kwargs)
        try:
            messwerte = Wetterdaten.objects.filter(
                datumzeit__gte=dt_begin_utc, datumzeit__lt=dt_end_utc).order_by('-datumzeit')
            context.update({'form': form})
            context.update({'errors': ''})
            if messwerte:
                context.update({'actual_date': messwerte.datumzeit})
                context.update({'has_data': messwerte.count() > 0})
                context.update({'messwerte': messwerte})
        except Exception:
            logger.error("get data form database failed", exc_info=True)

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = SelectDateForm(data=request.POST)
        context = super().get_context_data()
        db_error = None
        if form.is_valid():
            datum = form.cleaned_data['datum']
            dt = datetime(year=datum.year, month=datum.month, day=datum.day)
            dt_utc = dt.astimezone(tz=timezone.utc)
            dt_end_utc = dt_utc + timedelta(days=1)
            try:
                messwerte = Wetterdaten.objects.filter(
                    datumzeit__gte=dt_utc, datumzeit__lt=dt_end_utc).order_by('-datumzeit')

                context.update({'form': form})
                context.update({'messwerte': messwerte})
                context.update({'actual_date': datum})
                context.update({'has_data': messwerte.count() > 0})
                return self.render_to_response(context)
            except Exception:
                logger.error("Unexpected failure", exc_info=True)
                db_error = ex.args[0]

        errors = list()
        if db_error:
            errors.append(db_error)
        errors.append("Ungültige Eingabe")
        context.update({'errors': errors})
        context.update({'form': form})
        return self.render_to_response(context)
