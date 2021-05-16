from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import re_path
from django.views import defaults as default_views

from first.views import FirstPage

urlpatterns = [
                  re_path(r'^$', FirstPage.as_view(), name="first"),
                  re_path(r'^i18n/', include('django.conf.urls.i18n')),
                  re_path(r'^login/$', auth_views.LoginView.as_view(), name='login'),
                  re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
                  re_path(r'^admin/', admin.site.urls),
                  re_path(r'^energie/', include('energie.urls', namespace='energie')),
                  # url(r'^tph/', include('tph.urls', namespace='tph')),
                  re_path(r'^wetterdaten/', include('wetterdaten.urls', namespace='wetterdaten')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        re_path(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        re_path(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        re_path(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        re_path(r'^500/$', default_views.server_error),
    ]
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
                          re_path(r'^__debug__/', include(debug_toolbar.urls)),
                      ] + urlpatterns

