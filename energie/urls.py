from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from energie.api.views import SmartMeterList
from energie.views import (EnergyOverview, Produktion, PvProduktionVerbrauch,
                           MesswerteView, Heizung, AktuelleDaten)

app_name = 'energie'

urlpatterns = [
    path('smdata/', SmartMeterList.as_view(), name='smdata'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('overview', EnergyOverview.as_view(), name='EnergyOverview'),
    path('produktion', Produktion.as_view(), name='produktion'),
    path('aktuelleDaten', AktuelleDaten.as_view(), name='aktuelleDaten'),
    path('pvProduktionVerbrauch', PvProduktionVerbrauch.as_view(), name='pvProduktionVerbrauch'),
    path('messwerte', MesswerteView.as_view(), name='messwerte'),
    path('heizung', Heizung.as_view(), name='heizung'),
]
