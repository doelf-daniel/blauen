from datetime import datetime, timedelta

import pytest
import pytz

from wetterdaten.models import Wetterdaten


@pytest.fixture
@pytest.mark.django_db
def create_some_wetterdaten_records():
    dtutc = datetime.utcnow()
    dt = pytz.timezone("Europe/Zurich").localize(dtutc)
    wd = Wetterdaten(datumzeit=dt, t=22.2, p=858, h=45.3, vbatt=3.87, status=0)
    wd.save()
    dt = dt + timedelta(hours=1)
    wd = Wetterdaten(datumzeit=dt, t=23.2, p=855, h=45.3, vbatt=3.87, status=0)
    wd.save()
    dt = dt + timedelta(hours=1)
    wd = Wetterdaten(datumzeit=dt, t=24.2, p=857, h=65.3, vbatt=3.87, status=0)
    wd.save()
    dt = dt + timedelta(hours=1)
    wd = Wetterdaten(datumzeit=dt, t=25.2, p=864, h=75.3, vbatt=3.87, status=0)
    wd.save()
    dt = dt + timedelta(hours=1)
    wd = Wetterdaten(datumzeit=dt, t=26.2, p=880, h=85.3, vbatt=3.87, status=0)
    wd.save()
