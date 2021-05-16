from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from .api.views import WetterDatenList
from .views import WetterdatenChartsView, WetterdatenAktuellView, WetterDatenListeTag

app_name = 'wetterdaten'

# router = routers.DefaultRouter()
# router.register(r'api', WetterdatenViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('wetterdaten/', WetterDatenList.as_view(), name='wetterdaten'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('daten/', WetterdatenChartsView.as_view(), name="chart"),
    path('daten_liste_tag/', WetterDatenListeTag.as_view(), name="daten_liste_tag"),
    path('aktuelleDaten/', WetterdatenAktuellView.as_view(), name="letzteWetterdaten"),
]
