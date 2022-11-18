from datetime import datetime, timedelta

import pytest
import pytz

from wetterdaten.weather_chart import create_dataframe


@pytest.mark.django_db(transaction=True)
def test_create_dataframe_1(create_some_wetterdaten_records):
    dtutc = datetime.utcnow() - timedelta(hours=1)
    dt_begin = pytz.timezone("Europe/Zurich").localize(dtutc)
    dt_end = dt_begin + timedelta(hours=20)
    create_dataframe(dt_begin, dt_end)
    pass
