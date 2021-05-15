import json
from copy import copy

import pytest
import rest_framework
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from energie.api.serializers import SmartMeterDatenSerializer
from energie.api.views import SmartMeterList

factory = APIRequestFactory()

JSON_ERROR = 'JSON parse error - Expecting value:'

data_dict = {
    "dt": "2020-05-22T11:09:36.762953+02:00",
    "active_power_p": 1.0,
    "active_power_m": 1.722,
    "reactive_power_p": 0.033,
    "reactive_power_m": 3.0,
    "apparent_power_p": 4.0,
    "apparent_power_m": 1.722,
    "power_factor": 1.0,
    "supply_frequency": 5.0,
    "active_energy_p": 1868.372,
    "active_energy_m": 4380.269,
    "reactive_energy_p": 84.617,
    "reactive_energy_m": 228.271,
    "apparent_energy_p": 1912.645,
    "apparent_energy_m": 4386.288
}


def test_valid_serializer():
    """
        "dt"   Problem: Angabe der Zeitzone

    """
    serializer = SmartMeterDatenSerializer(data=data_dict)
    assert serializer.is_valid()
    for key in data_dict.keys():
        if key != 'dt':
            assert serializer.validated_data.get(key) == data_dict.get(key)
    assert serializer.errors == {}


def test_valid_serializer_2():
    """
        "dt"   Problem: Angabe der Zeitzone

    """
    serializer = SmartMeterDatenSerializer(data=data_dict)
    assert serializer.is_valid()
    assert serializer.errors == {}


def test_valid_serializer_none():
    """
        "dt"   Problem: Angabe der Zeitzone

    """
    dd = copy(data_dict)
    dd['active_power_p'] = None
    serializer = SmartMeterDatenSerializer(data=dd)
    assert not serializer.is_valid()
    assert len(serializer.errors) > 0
    assert type(serializer.errors['active_power_p'][0]) == rest_framework.exceptions.ErrorDetail


def test_post_unauthorized():
    view = SmartMeterList.as_view()
    request = factory.post('/', json.dumps(data_dict), content_type='application/json')
    response = view(request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_post_authorized():
    view = SmartMeterList.as_view()
    request = factory.post('/', json.dumps(data_dict), content_type='application/json')
    User.objects.create(first_name="Max", last_name="Meier", username="meier19")
    user = User.objects.get(username='meier19')
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == status.HTTP_201_CREATED
