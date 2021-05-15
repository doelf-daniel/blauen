from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

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


class SmartMeterTests(APITestCase):
    def test_create_smdata_unauthorized(self):
        url = reverse('energie:smdata')
        data = data_dict
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_smdata_unauthorized2(self):
        url = reverse('energie:smdata')
        data = data_dict
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
