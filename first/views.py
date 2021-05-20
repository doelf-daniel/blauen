import base64
import logging
from datetime import timedelta, datetime
from io import BytesIO

# Create your views here.
from django.views.generic import TemplateView

from config.settings.common import TZ
from energie.energie_sets_factory import create_energy_set_per_week, create_energy_set_per_day, \
    create_energy_set_actual_year
from energie.power_chart import create_power_chart
from wetterdaten.weather_chart import pressure_chart, temperature_chart

logger = logging.getLogger(__name__)


class FirstPage(TemplateView):
    template_name = "first/first_page.html"

    def get(self, request, *args, **kwargs):
        dt_end = datetime.now(tz=TZ)
        dt_begin = dt_end - timedelta(days=7)
        dt_begin.replace(hour=0)
        dt_begin.replace(minute=0)
        dt_begin.replace(second=0)
        # Temperatur Chart
        fig = temperature_chart(dt_begin, dt_end)
        context = super(FirstPage, self).get_context_data(**kwargs)

        if fig is not None:
            try:
                buf = BytesIO()
                fig.savefig(buf, format='png')
                image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
                buf.close()
                context.update({'image_base64_1': image_base64})
                context.update({'data1': 'has_data'})
            except Exception as ex:
                logger.error("Bilddatei nicht gefunden!", ex)
        else:
            context.update({'data1': 'has no data'})
            logger.error("Bilddatei1 nicht gefunden!")
        # Luftdruck Chart
        fig2 = pressure_chart(dt_begin, dt_end)
        if fig2 is not None:
            try:
                buf = BytesIO()
                fig2.savefig(buf, format='png')
                image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
                buf.close()
                context.update({'image_base64_2': image_base64})
                context.update({'data2': 'has_data'})
            except Exception as ex:
                context.update({'data2': 'has no data'})
                logger.error("Bilddatei2 nicht gefunden!", ex)
        else:
            context.update({'data2': 'has no data'})
            logger.error("Bilddatei1 nicht gefunden!")
        # Strom Chart
        try:
            dt_begin = dt_end - timedelta(days=2)
            dt_begin.replace(hour=0)
            dt_begin.replace(minute=0)
            dt_begin.replace(second=0)
            fig = create_power_chart(dt_begin, dt_end)
            if fig is not None:
                try:
                    buf = BytesIO()
                    fig.savefig(buf, format='png')
                    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
                    buf.close()
                    context.update({'image_base64_3': image_base64})
                    context.update({'data3': 'has_data'})
                except Exception as ex:
                    logger.error("Bilddatei nicht gefunden!", ex)
            else:
                context.update({'data3': 'has no data'})
        except Exception as ex:
            logger.error("create_power_chart() failed", ex)
        # Produktion, Verbrauch
        eset_total = create_energy_set_actual_year(dt_end)
        eset_week1 = create_energy_set_per_week(dt_end, 1)
        eset_week2 = create_energy_set_per_week(dt_end, 2)
        eset_day1 = create_energy_set_per_day(dt_end)
        eset_day2 = create_energy_set_per_day(dt_end - timedelta(1))
        eset_day3 = create_energy_set_per_day(dt_end - timedelta(2))
        context.update({'eset_total': eset_total})
        context.update({'eset_week1': eset_week1})
        context.update({'eset_week2': eset_week2})
        context.update({'eset_day1': eset_day1})
        context.update({'eset_day2': eset_day2})
        context.update({'eset_day3': eset_day3})

        return self.render_to_response(context)
