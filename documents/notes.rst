**************
Projekt Blauen
**************

Referenzen
==========

Creating bitmap charts in Django with the ReportLab library
https://code.djangoproject.com/wiki/Charts

ReportTools: Google Charts
https://django-report-tools.readthedocs.io/en/latest/renderers/googlecharts/


Create a Dashboard using Highcharts and Django:
https://www.highcharts.com/blog/post/create-a-dashboard-using-highcharts-and-django/

Restframework
=============

URL:  http://localhost:8000/tph/tphdata/

..  figure:: ./images/rest_1.png
    :scale: 80%
    :align: center

|


Test mit curl
::

    [doelf@mars ~]$ curl -H "Content-Type: application/json" --request POST \
    --data '{"created": "2020-02-01T01:02:00Z","t_innen": 22.3,"t_aussen": 11.3,"p": 1000.3,"h": 50.3 }' \
    http://localhost:8000/tph/tphdata/


Die Daten wurden in der Datenbank gespeichert.

Test mit http (httpie)

::

    [doelf@mars ~]$ http POST http://localhost:8000/tph/tphdata/ created=2020-02-01T01:02:00Z t_innen=22.3 t_aussen=11.3 p=1000.3 h=50.3
    HTTP/1.1 201 Created
    Allow: GET, POST, HEAD, OPTIONS
    Content-Language: en
    Content-Length: 98
    Content-Type: application/json
    Date: Sat, 02 Nov 2019 00:06:05 GMT
    Server: WSGIServer/0.2 CPython/3.7.4
    Vary: Accept, Accept-Language, Cookie
    X-Frame-Options: SAMEORIGIN

    {
        "created": "2020-02-01T01:02:00Z",
        "h": 50.3,
        "id": 1581012,
        "p": 1000.3,
        "t_aussen": 11.3,
        "t_innen": 22.3
    }

    [doelf@mars ~]$

Create a token
--------------

::

    manage.py@blauen > drf_create_token doelf
    bash -cl "/home/doelf/.virtualenv/blauen/bin/python3.7 /home/doelf/bin/pycharm-2019.2/helpers/pycharm/django_manage.py drf_create_token doelf /home/doelf/dev/django/blauen"
    /home/doelf/.bashrc: line 30: export: `/home/doelf/esp/esp-idf': not a valid identifier
    Tracking file by folder pattern:  migrations
    Generated token 55eebd68f9d4625a3b39796881348cdec18fe98a for user doelf
    Process finished with exit code 0

::

    [doelf@mars ~]$ http http://127.0.0.1:8000/tph/tph/
    HTTP/1.1 401 Unauthorized
    Allow: GET, POST, HEAD, OPTIONS
    Content-Language: en
    Content-Length: 58
    Content-Type: application/json
    Date: Tue, 22 Oct 2019 20:22:49 GMT
    Server: WSGIServer/0.2 CPython/3.7.4
    Vary: Accept, Accept-Language, Cookie
    WWW-Authenticate: Token
    X-Frame-Options: SAMEORIGIN

    {
        "detail": "Authentication credentials were not provided."
    }

    [doelf@mars ~]$ http http://127.0.0.1:8000/tph/tph/ 'Authorization: Token 55eebd68f9d4625a3b39796881348cdec18fe98a'
    HTTP/1.1 200 OK
    Allow: GET, POST, HEAD, OPTIONS
    Content-Language: en
    Content-Length: 52
    Content-Type: application/json
    Date: Tue, 22 Oct 2019 20:24:57 GMT
    Server: WSGIServer/0.2 CPython/3.7.4
    Vary: Accept, Accept-Language, Cookie
    X-Frame-Options: SAMEORIGIN

    {
        "count": 0,
        "next": null,
        "previous": null,
        "results": []
    }

    [doelf@mars ~]$


::

    [doelf@mars ~]$ http http://127.0.0.1:8000/tph/tph/ 'Authorization: Token 55eebd68f9d4625a3b39796881348cdec18fe98a'
    HTTP/1.1 200 OK
    Allow: GET, POST, HEAD, OPTIONS
    Content-Language: en
    Content-Length: 795
    Content-Type: application/json
    Date: Tue, 22 Oct 2019 21:00:15 GMT
    Server: WSGIServer/0.2 CPython/3.7.4
    Vary: Accept, Accept-Language, Cookie
    X-Frame-Options: SAMEORIGIN

    {
        "count": 8,
        "next": null,
        "previous": null,
        "results": [
            {
                "created": "2000-01-01T09:10:00Z",
                "h": 55.2,
                "id": 5,
                "p": 1002.2,
                "t_aussen": 13.2,
                "t_innen": 23.4
            },
            {
                "created": "2000-01-01T09:36:00Z",
                "h": 55.2,
                "id": 4,
                "p": 1002.2,
                "t_aussen": 13.2,
                "t_innen": 23.4
            },
            {
                "created": "2000-01-01T10:10:00Z",
                "h": 55.2,
                "id": 1,
                "p": 1002.2,
                "t_aussen": 13.2,
                "t_innen": 23.4
            },
            {
                "created": "2000-01-01T10:10:10Z",
                "h": 55.4,
                "id": 2,
                "p": 1003.2,
                "t_aussen": 13.5,
                "t_innen": 23.3
            },
            {
                "created": "2000-01-01T10:10:20Z",
                "h": 55.4,
                "id": 3,
                "p": 1003.2,
                "t_aussen": 13.5,
                "t_innen": 23.3
            },
            {
                "created": "2000-01-01T11:10:00Z",
                "h": 55.2,
                "id": 6,
                "p": 1002.2,
                "t_aussen": 13.2,
                "t_innen": 23.4
            },
            {
                "created": "2000-01-01T11:10:10Z",
                "h": 55.4,
                "id": 7,
                "p": 1003.2,
                "t_aussen": 13.5,
                "t_innen": 23.3
            },
            {
                "created": "2000-01-01T11:10:20Z",
                "h": 55.4,
                "id": 8,
                "p": 1003.2,
                "t_aussen": 13.5,
                "t_innen": 23.3
            }
        ]
    }

    [doelf@mars ~]$

REST-API: Energie
=================

Erster Test:

::

    [doelf@mars ~]$ curl -v  http://127.0.0.1:8000/energie/api/
    *   Trying 127.0.0.1:8000...
    * TCP_NODELAY set
    * Connected to 127.0.0.1 (127.0.0.1) port 8000 (#0)
    > GET /energie/api/ HTTP/1.1
    > Host: 127.0.0.1:8000
    > User-Agent: curl/7.66.0
    > Accept: */*
    >
    * Mark bundle as not supporting multiuse
    < HTTP/1.1 200 OK
    < Date: Wed, 15 Apr 2020 21:29:30 GMT
    < Server: WSGIServer/0.2 CPython/3.7.6
    < Content-Type: application/json
    < Vary: Accept, Accept-Language
    < Allow: GET, POST, HEAD, OPTIONS
    < X-Frame-Options: DENY
    < Content-Length: 4158
    < Content-Language: en
    < X-Content-Type-Options: nosniff
    <
    { "count":24367,
      "next":"http://127.0.0.1:8000/energie/api/?page=2","previous":null,"results":
        [
            {
                "id":1,
                "dt":"2020-02-24T15:29:55.174289+01:00",
                "active_power_p":0.0,
                "active_power_m":7.4526,
                "reactive_power_p":0.0,
                "reactive_power_m":0.1228,
                "apparent_power_p":0.0,
                "apparent_power_m":7.4536,
                "power_factor":1.0,
                "supply_frequency":49.975,
                "active_energy_p":1037.9595,
                "active_energy_m":918.6634,
                "reactive_energy_p":40.4069,
                "reactive_energy_m":94.7634,
                "apparent_energy_p":1056.7776,
                "apparent_energy_m":921.1386
            },
            ..............


::

    [doelf@mars ~]$ http --json GET  http://localhost:8000/energie/api/
    HTTP/1.1 200 OK
    Allow: GET, POST, HEAD, OPTIONS
    Content-Language: en
    Content-Length: 4158
    Content-Type: application/json
    Date: Wed, 15 Apr 2020 21:45:45 GMT
    Server: WSGIServer/0.2 CPython/3.7.6
    Vary: Accept, Accept-Language
    X-Content-Type-Options: nosniff
    X-Frame-Options: DENY

    {
        "count": 24367,
        "next": "http://localhost:8000/energie/api/?page=2",
        "previous": null,
        "results": [
            {
                "active_energy_m": 918.6634,
                "active_energy_p": 1037.9595,
                "active_power_m": 7.4526,
                "active_power_p": 0.0,
                "apparent_energy_m": 921.1386,
                "apparent_energy_p": 1056.7776,
                "apparent_power_m": 7.4536,
                "apparent_power_p": 0.0,
                "dt": "2020-02-24T15:29:55.174289+01:00",
                "id": 1,
                "power_factor": 1.0,
                "reactive_energy_m": 94.7634,
                "reactive_energy_p": 40.4069,
                "reactive_power_m": 0.1228,
                "reactive_power_p": 0.0,
                "supply_frequency": 49.975
            },
            {
                "active_energy_m": 918.9118,
                "active_energy_p": 1037.9595,
                "active_power_m": 7.4473,
                "active_power_p": 0.0,
                "apparent_energy_m": 921.387,
                "apparent_energy_p": 1056.7776,
                "apparent_power_m": 7.4479,
                "apparent_power_p": 0.0,
                "dt": "2020-02-24T15:31:55.175454+01:00",
                "id": 2,
                "power_factor": 1.0,
                "reactive_energy_m": 94.7652,
                "reactive_energy_p": 40.4078,
                "reactive_power_m": 0.0,
                "reactive_power_p": 0.0951,
                "supply_frequency": 49.97
            },
            {
                "active_energy_m": 919.1586,
                "active_energy_p": 1037.9595,
                "active_power_m": 7.3815,
                "active_power_p": 0.0,
                "apparent_energy_m": 921.6338,
                "apparent_energy_p": 1056.7776,
                "apparent_power_m": 7.3824,
                "apparent_power_p": 0.0,
                "dt": "2020-02-24T15:33:55.175892+01:00",
                "id": 3,
                "power_factor": 1.0,
                "reactive_energy_m": 94.7669,
                "reactive_energy_p": 40.4088,
                "reactive_power_m": 0.117,
                "reactive_power_p": 0.0,
                "supply_frequency": 49.984
            },
            {
                "active_energy_m": 919.4039,
                "active_energy_p": 1037.9595,
                "active_power_m": 7.3394,
                "active_power_p": 0.0,
                "apparent_energy_m": 921.8791,
                "apparent_energy_p": 1056.7776,
                "apparent_power_m": 7.3395,
                "apparent_power_p": 0.0,
                "dt": "2020-02-24T15:35:55.171979+01:00",
                "id": 4,
                "power_factor": 1.0,
                "reactive_energy_m": 94.7686,
                "reactive_energy_p": 40.4098,
                "reactive_power_m": 0.0,
                "reactive_power_p": 0.0296,
                "supply_frequency": 49.968
            },
            {
                "active_energy_m": 919.6475,
                "active_energy_p": 1037.9595,
                "active_power_m": 7.2704,
                "active_power_p": 0.0,
                "apparent_energy_m": 922.1227,
                "apparent_energy_p": 1056.7776,
                "apparent_power_m": 7.2704,
                "apparent_power_p": 0.0,
                "dt": "2020-02-24T15:37:55.153982+01:00",
                "id": 5,
                "power_factor": 1.0,
                "reactive_energy_m": 94.7703,
                "reactive_energy_p": 40.4107,
                "reactive_power_m": 0.0,
                "reactive_power_p": 0.003,
                "supply_frequency": 49.972
            },
            {
                "active_energy_m": 919.8871,
                "active_energy_p": 1037.9595,
                "active_power_m": 7.1867,
                "active_power_p": 0.0,
                "apparent_energy_m": 922.3623,
                "apparent_energy_p": 1056.7776,
                "apparent_power_m": 7.1877,
                "apparent_power_p": 0.0,
                "dt": "2020-02-24T15:39:55.126590+01:00",
                "id": 6,
                "power_factor": 1.0,
                "reactive_energy_m": 94.7721,
                "reactive_energy_p": 40.4117,
                "reactive_power_m": 0.1247,
                "reactive_power_p": 0.0,
                "supply_frequency": 49.986
            },
            {
                "active_energy_m": 920.1256,
                "active_energy_p": 1037.9595,
                "active_power_m": 7.1385,
                "active_power_p": 0.0,
                "apparent_energy_m": 922.6019,
                "apparent_energy_p": 1056.7776,
                "apparent_power_m": 7.1391,
                "apparent_power_p": 0.0,
                "dt": "2020-02-24T15:41:55.175441+01:00",
                "id": 7,
                "power_factor": 1.0,
                "reactive_energy_m": 94.7737,
                "reactive_energy_p": 40.4126,
                "reactive_power_m": 0.0,
                "reactive_power_p": 0.0928,
                "supply_frequency": 49.963
            },
            {
                "active_energy_m": 920.3632,
                "active_energy_p": 1037.9595,
                "active_power_m": 7.1111,
                "active_power_p": 0.0,
                "apparent_energy_m": 922.8385,
                "apparent_energy_p": 1056.7776,
                "apparent_power_m": 7.112,
                "apparent_power_p": 0.0,
                "dt": "2020-02-24T15:43:55.129767+01:00",
                "id": 8,
                "power_factor": 1.0,
                "reactive_energy_m": 94.7754,
                "reactive_energy_p": 40.4135,
                "reactive_power_m": 0.1103,
                "reactive_power_p": 0.0,
                "supply_frequency": 50.002
            },
            {
                "active_energy_m": 920.5996,
                "active_energy_p": 1037.9595,
                "active_power_m": 7.0168,
                "active_power_p": 0.0,
                "apparent_energy_m": 923.075,
                "apparent_energy_p": 1056.7776,
                "apparent_power_m": 7.0168,
                "apparent_power_p": 0.0,
                "dt": "2020-02-24T15:45:55.146801+01:00",
                "id": 9,
                "power_factor": 1.0,
                "reactive_energy_m": 94.7771,
                "reactive_energy_p": 40.4145,
                "reactive_power_m": 0.0,
                "reactive_power_p": 0.0222,
                "supply_frequency": 50.01
            },
            {
                "active_energy_m": 920.8332,
                "active_energy_p": 1037.9595,
                "active_power_m": 6.9762,
                "active_power_p": 0.0,
                "apparent_energy_m": 923.3086,
                "apparent_energy_p": 1056.7776,
                "apparent_power_m": 6.9764,
                "apparent_power_p": 0.0,
                "dt": "2020-02-24T15:47:55.175486+01:00",
                "id": 10,
                "power_factor": 1.0,
                "reactive_energy_m": 94.7788,
                "reactive_energy_p": 40.4154,
                "reactive_power_m": 0.0,
                "reactive_power_p": 0.0385,
                "supply_frequency": 49.983
            }
        ]
    }

    [doelf@mars ~]$

Daten einfügen mit POST:

::

    [doelf@mars ~]$ curl -H "Content-Type: application/json" --request POST --data \
        '{"dt": "2020-04-15 23:57:51.788124", "active_power_p": 0.315, "active_power_m": 0, "reactive_power_p": 0, \
            "reactive_power_m": 0.067, "apparent_power_p": 0.322, "apparent_power_m": 0, "power_factor": 0.978, \
            "reactive_energy_p": 68.134, "reactive_energy_m": 168.099, "apparent_energy_p": 1608.565, \
            "apparent_energy_m": 2854.68 }' http://localhost:8000/energie/api/
     -->
    {"id":24375,"dt":"2020-04-15T23:59:51.788124+02:00","active_power_p":0.315,"active_power_m":0.0,
    "reactive_power_p":0.0,"reactive_power_m":0.067,"apparent_power_p":0.322,"apparent_power_m":0.0,
    "power_factor":0.978,"supply_frequency":0.0,"active_energy_p":0.0,"active_energy_m":0.0,
    "reactive_energy_p":68.134,"reactive_energy_m":168.099,"apparent_energy_p":1608.565,
    "apparent_energy_m":2854.68}[doelf@mars ~]$







Create Database
===============

::

    postgres=# CREATE DATABASE doelf_blauen ENCODING ’UTF8’ TEMPLATE=template0 OWNER doelf;
    CREATE DATABASE
    postgres=#

Authentizierung
===============

Dazu wurde die Klasse ElektrizitatsdatenView von

::

    class ElektrizitaetsdatenViewSet(ModelViewSet):
        authentication_classes = []
        permission_classes = []
        queryset = SmartMeter.objects.all().order_by('id')
        serializer_class = SmartMeterDatenSerializer

geändert in:

::

    class ElektrizitaetsdatenViewSet(ModelViewSet):
        authentication_classes = [TokenAuthentication]
        permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        queryset = SmartMeter.objects.all().order_by('id')
        serializer_class = SmartMeterDatenSerializer

Test mit curl:

::

    [doelf@mars ~]$ curl -H "Content-Type: application/json" --request POST \
            --data '{"dt": "2020-04-16 12:57:35.222653", "active_power_p": 0, "active_power_m": 5.182, \
            "reactive_power_p": 0, "reactive_power_m": 0.008, "apparent_power_p": 0, \
            "apparent_power_m": 5.182, "power_factor": 1.0, "reactive_energy_p": 68.61, \
            "reactive_energy_m": 168.623, "apparent_energy_p": 1614.846, "apparent_energy_m": 2869.082 }' \
            http://localhost:8000/energie/api/
    {"detail":"Authentication credentials were not provided."}[doelf@mars ~]$


::

    [doelf@mars ~]$ curl -H "Content-Type: application/json" \
                    -H  "Authorization: Token 79b4c72fe5a2b3d0e11cf2e737f5f2581cb43e4b"  \
                    --request POST \
                    --data '{"dt": "2020-04-16 12:57:36.222653", "active_power_p": 0, "active_power_m": 5.182, \
                        "reactive_power_p": 0, "reactive_power_m": 0.008, "apparent_power_p": 0, "apparent_power_m": 5.182,\
                        "power_factor": 1.0, "reactive_energy_p": 68.61, "reactive_energy_m": 168.623, "\
                        apparent_energy_p": 1614.846, "apparent_energy_m": 2869.082 }' \
                    http://localhost:8000/energie/api/


Token
-----


::

    [doelf@mars ~]$ http post http://127.0.0.1:8000/energie/api-token-auth/ username=doelf password=x12k7A23
    HTTP/1.1 200 OK
    Allow: POST, OPTIONS
    Content-Language: en
    Content-Length: 52
    Content-Type: application/json
    Date: Thu, 16 Apr 2020 15:16:25 GMT
    Server: WSGIServer/0.2 CPython/3.7.6
    Vary: Accept-Language
    X-Content-Type-Options: nosniff
    X-Frame-Options: DENY

    {
        "token": "79b4c72fe5a2b3d0e11cf2e737f5f2581cb43e4b"
    }

    [doelf@mars ~]$




Entwicklung
===========

Datenbank-Problem
-----------------

Auf Django-Europe war es nicht mehr möglich die Datenbank des Modules Energie zu migrieren. Das Problem konnte wie
folgt behoben werden:

::

    python manage.py migrate --fake energie zero
    # This reset all migrations (to the zeroth state)
    # This followed by :
    python manage.py migrate energie

Compile scss Files
------------------

Im Vereichnis   /home/doelf/dev/django/blauen/dproject/static

::

    sass --watch ./scss/:./css/


ODER

::

    (.venv) [doelf@linux static]$ scss --watch ./scss:./css
    >>> Sass is watching for changes. Press Ctrl-C to stop.
          write ./css/project.css
          write ./css/project.css.map
          write ./css/pth.css
          write ./css/pth.css.map


Filter and Paging
-----------------

https://www.caktusgroup.com/blog/2018/10/18/filtering-and-pagination-django/


Django Filtering System with django-filter - Filter Queryset (2018)
https://github.com/TheDumbfounds/snippetproject-basic
