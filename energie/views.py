import base64
import logging
from datetime import datetime, timedelta
from io import BytesIO

from django.http import JsonResponse
from django.utils import timezone
from django.views.generic import TemplateView
from pandas.plotting import register_matplotlib_converters
from qsstats import QuerySetStats

from common.datetime_functions import begin_of_week_with_date, begin_of_month_with_date, begin_month_before
from config.settings.common import TZ
from energie.forms import SelectFormEnergieChart, PROD_PERIOD_2, PROD_PERIOD_3, SelectFormEnergieTables, \
    TABLE_PERIOD_DAYS, SelectFormMesswerte, TABLE_PERIOD_WEEKS, TABLE_PERIOD_MONTHS
from energie.models import SmartMeter
from energie.periodic_data import PeriodicData
from energie.power_chart import create_power_chart

register_matplotlib_converters()

logger = logging.getLogger(__name__)


class EnergyOverview(TemplateView):
    template_name = 'energie/overview.html'


def time_series(queryset, date_field, interval, func=None):
    qsstats = QuerySetStats(queryset, date_field, func)
    return qsstats.time_series(*interval)


class Produktion(TemplateView):
    template_name = 'energie/produktion.html'

    @classmethod
    def create_filter_dict(cls, dauer, ende):
        filter_dict = dict()
        filter_dict['dauer'] = dauer
        filter_dict['ende'] = ende
        return filter_dict

    @classmethod
    def pass_fig(cls, fig, context):
        if fig is not None:
            try:
                buf = BytesIO()
                fig.savefig(buf, format='png')
                image_base64 = base64.b64encode(
                    buf.getvalue()).decode('utf-8').replace('\n', '')
                buf.close()
                context.update({'image_base64_1': image_base64})
                context.update({'data': 'has_data'})
            except Exception as ex:
                logger.warning("Bilddatei nicht gefunden!", ex)
        else:
            context.update({'data': 'has no data'})

    def get(self, request, *args, **kwargs):
        dt_end = datetime.now(tz=TZ)
        dt_begin = datetime(dt_end.year, dt_end.month,
                            dt_end.day, 0, 0, 0, tzinfo=TZ) - timedelta(days=1)
        dt_begin.replace(hour=0)
        dt_begin.replace(minute=0)
        dt_begin.replace(second=0)
        filter_dict = self.create_filter_dict(1, dt_end)
        form = SelectFormEnergieChart(initial=filter_dict)
        context = super().get_context_data(**kwargs)
        context.update({'form': form})
        try:
            fig = create_power_chart(dt_begin, dt_end)
            self.pass_fig(fig, context)
        except Exception as ex:
            logger.error("create_power_chart() failed", ex)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = SelectFormEnergieChart(data=request.POST)
        context = super().get_context_data()
        if form.is_valid():
            end_date = form.cleaned_data['ende']
            end_dt = datetime(end_date.year, end_date.month,
                              end_date.day, 23, 59, 59, 999999, tzinfo=TZ)
            dauer = form.cleaned_data['dauer']
            begin_dt = self.calculate_begin(end_dt, dauer)
            # neue Werte aufgrund der Auswahl
            filter_dict = self.create_filter_dict(dauer, end_date)

            form = SelectFormEnergieChart(initial=filter_dict)
            fig = create_power_chart(begin_dt, end_dt)
            context = super(Produktion,
                            self).get_context_data(**kwargs)
            self.pass_fig(fig, context)
        else:
            logger.warning("invalid form")

        context.update({'form': form})
        return self.render_to_response(context)

    @staticmethod
    def calculate_begin(end_date, dauer):
        if dauer == PROD_PERIOD_2:
            days = 3
        elif dauer == PROD_PERIOD_3:
            days = 7
        else:
            days = 1
        beginn = end_date + timedelta(microseconds=1) - timedelta(days=days + 1)
        return beginn


class Heizung(TemplateView):
    template_name = "energie/heizung.html"


class PvProduktionVerbrauch(TemplateView):
    """
        Darstellung der Produktions- und Verbrauchsdaten in einer Tabelle

    """
    template_name = 'energie/pvProduktionVerbrauch.html'

    @classmethod
    def create_filter_dict(cls, begin, end, period):
        filter_dict = dict()
        filter_dict['begin'] = begin
        filter_dict['end'] = end
        filter_dict['period'] = period
        return filter_dict

    @classmethod
    def process_filter_data(cls, dt0, dt1, period):
        """
         Aufgrund von dt_begin, dt_end und period werden dt0 effektiver Beginn und dt1 effektives Ende bestimmt.

        :param dt0:       Begin der Periode
        :param dt1:       Ende der Periode
        :param period:    Periode: TABLE_PERIOD_DAYS,TABLE_PERIOD_WEEKS, TABLE_MONTHS,
        :return: dt0, dt1
        """
        if period == TABLE_PERIOD_WEEKS:
            dt01 = begin_of_week_with_date(dt0)
            dt11 = begin_of_week_with_date(dt1)
            if dt01 == dt11:
                dt01 = dt11 - timedelta(days=7)
        elif period == TABLE_PERIOD_MONTHS:
            dt01 = begin_of_month_with_date(dt0)
            dt11 = begin_of_month_with_date(dt1)
            if dt01 == dt11 - begin_month_before(dt1):
                dt01 = begin_month_before(dt01)
        else:
            dt01 = dt0
            dt11 = dt1
        return dt01, dt11

    def get(self, request, *args, **kwargs):
        dt_end = datetime.now(tz=TZ)
        dt_begin = datetime(dt_end.year, dt_end.month,
                            dt_end.day, 0, 0, 0, tzinfo=TZ) - timedelta(days=10)
        dt_begin.replace(hour=0)
        dt_begin.replace(minute=0)
        dt_begin.replace(second=0)
        filter_dict = self.create_filter_dict(
            dt_begin, dt_end, TABLE_PERIOD_DAYS)
        form = SelectFormEnergieTables(initial=filter_dict)
        context = super().get_context_data(**kwargs)
        try:
            periodic_data = PeriodicData(dt_begin, dt_end, TABLE_PERIOD_DAYS)
            object_list = periodic_data.get_energyset_list()
            periodic_data = None
            context.update({'form': form})
            context.update({'erorrs': ''})
            context.update({'title': TABLE_PERIOD_DAYS})
            context.update({'object_list': object_list})
        except Exception as ex:
            logger.error("create_power_chart() failed", ex)

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = SelectFormEnergieTables(data=request.POST)
        context = super().get_context_data()
        db_error = None
        if form.is_valid():
            end_date = form.cleaned_data['end']
            begin_date = form.cleaned_data['begin']
            period = form.cleaned_data['period']
            dt1 = datetime(year=begin_date.year,
                           month=begin_date.month, day=begin_date.day, tzinfo=TZ)
            dt2 = datetime(year=end_date.year, month=end_date.month,
                           day=end_date.day, tzinfo=TZ)
            dt_begin, dt_end = self.process_filter_data(dt1, dt2, period)
            periodic_data = None
            try:
                if period == TABLE_PERIOD_DAYS:
                    # Read data from database
                    # periodic_data_list = PeriodicDataList(dt_begin, dt_end, period)
                    # object_list = periodic_data_list.get_list()
                    periodic_data = PeriodicData(
                        dt_begin, dt_end, TABLE_PERIOD_DAYS)
                    object_list = periodic_data.get_energyset_list()
                elif period == TABLE_PERIOD_WEEKS:
                    periodic_data = PeriodicData(
                        dt_begin, dt_end, TABLE_PERIOD_WEEKS)
                    object_list = periodic_data.get_energyset_list()
                elif period == TABLE_PERIOD_MONTHS:
                    periodic_data = PeriodicData(
                        dt_begin, dt_end, TABLE_PERIOD_MONTHS)
                    object_list = periodic_data.get_energyset_list()
                else:
                    object_list = list()
                context.update({'form': form})
                context.update({'title': period})
                context.update({'object_list': object_list})
                periodic_data = None
                return self.render_to_response(context)
            except Exception as ex:
                periodic_data = None
                logger.error("Unexpected failure", ex)
                db_error = ex.args[0]
        errors = list()
        if db_error:
            errors.append(db_error)
        errors.append("Ungültige Eingabe")
        context.update({'errors': errors})
        context.update({'form': form})
        return self.render_to_response(context)


class MesswerteView(TemplateView):
    template_name = 'energie/messwerte.html'
    # paginate_by = 15
    title = 'Zählerdaten eines Tages'

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
        filter_dict = self.create_filter_dict(dt_begin)
        form = SelectFormMesswerte(initial=filter_dict)
        context = super().get_context_data(**kwargs)
        try:
            messwerte = SmartMeter.objects.filter(
                dt__gte=dt_begin_utc, dt__lt=dt_end_utc).order_by('-dt')

            context.update({'form': form})
            context.update({'errors': ''})
            context.update({'title': self.title})
            context.update({'messwerte': messwerte})
        except Exception as ex:
            logger.error("create_power_chart() failed", ex)

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = SelectFormMesswerte(data=request.POST)
        context = super().get_context_data()
        db_error = None
        if form.is_valid():
            begin_date = form.cleaned_data['begin']
            dt_begin = datetime(begin_date.year, begin_date.month,
                                begin_date.day, 0, 0, 0, tzinfo=TZ)
            dt_end = dt_begin + timedelta(days=1)

            dt_begin_utc = dt_begin.astimezone(tz=timezone.utc)
            dt_end_utc = dt_end.astimezone(tz=timezone.utc)
            try:
                messwerte = SmartMeter.objects.filter(
                    dt__gte=dt_begin_utc, dt__lt=dt_end_utc).order_by('-dt')

                context.update({'form': form})
                context.update({'messwerte': messwerte})
                context.update({'title': self.title})
                return self.render_to_response(context)
            except Exception as ex:
                logger.error("Unexpected failure", ex)
                db_error = ex.args[0]

        errors = list()
        if db_error:
            errors.append(db_error)
        errors.append("Ungültige Eingabe")
        context.update({'errors': errors})
        context.update({'form': form})
        return self.render_to_response(context)


class AktuelleDaten(TemplateView):
    template_name = "energie/aktuelleDaten.html"

    def find_data(self, dt):
        messwerte = SmartMeter.objects.filter(dt__lte=dt).order_by('-dt').first()

        dt_str = dt.strftime("%d.%m.%Y  %H:%M:%S")
        data = {'datum_zeit': dt_str,
                'active_power_m': "{:.3f}".format(messwerte.active_power_m),
                'active_power_p': "{:.3f}".format(messwerte.active_power_p),
                'active_energy_m': "{:.1f}".format(messwerte.active_energy_m),
                'active_energy_p': "{:.1f}".format(messwerte.active_energy_p),
                }
        return data

    def get(self, request, *args, **kwargs):
        dt = datetime.now(tz=TZ)
        if request.is_ajax():
            data = self.find_data(dt)
            return JsonResponse(data, status=200)

        context = super().get_context_data(**kwargs)
        data = self.find_data(dt)
        context.update({'data': data})
        return self.render_to_response(context)
