# Gunicorn




## Running Gunicorn (Socket-Version)

        (blauen) doelf@neptun:~/bin/blauen$ sh ./gunicorn_socke_start.sh 
        Starting blauen as doelf
        ./gunicorn_socke_start.sh: 21: source: not found
        PYTHONPATH: /home/doelf/bin/blauen:/home/doelf/.local/virtualenv/blauen/bin
        
        [2022-11-25 00:20:41 +0100] [13821] [DEBUG] Current configuration:
          config: ./gunicorn.conf.py
          wsgi_app: None
          bind: ['unix:/home/doelf/bin/blauen/run/gunicorn.sock']
          backlog: 2048
          workers: 3
          worker_class: sync
          threads: 1
          worker_connections: 1000
          max_requests: 0
          max_requests_jitter: 0
          timeout: 30
          graceful_timeout: 30
          keepalive: 2
          limit_request_line: 4094
          limit_request_fields: 100
          limit_request_field_size: 8190
          reload: False
          reload_engine: auto
          reload_extra_files: []
          spew: False
          check_config: False
          print_config: False
          preload_app: False
          sendfile: None
          reuse_port: False
          chdir: /home/doelf/bin/blauen
          daemon: False
          raw_env: []
          pidfile: None
          worker_tmp_dir: None
          user: 1000
          group: 1000
          umask: 0
          initgroups: False
          tmp_upload_dir: None
          secure_scheme_headers: {'X-FORWARDED-PROTOCOL': 'ssl', 'X-FORWARDED-PROTO': 'https', 'X-FORWARDED-SSL': 'on'}
          forwarded_allow_ips: ['127.0.0.1']
          accesslog: None
          disable_redirect_access_to_syslog: False
          access_log_format: %(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"
          errorlog: -
          loglevel: debug
          capture_output: False
          logger_class: gunicorn.glogging.Logger
          logconfig: None
          logconfig_dict: {}
          syslog_addr: udp://localhost:514
          syslog: False
          syslog_prefix: None
          syslog_facility: user
          enable_stdio_inheritance: False
          statsd_host: None
          dogstatsd_tags: 
          statsd_prefix: 
          proc_name: blauen
          default_proc_name: blauen.wsgi:application
          pythonpath: None
          paste: None
          on_starting: <function OnStarting.on_starting at 0x7fed60cbfe20>
          on_reload: <function OnReload.on_reload at 0x7fed60cbff40>
          when_ready: <function WhenReady.when_ready at 0x7fed60cd80d0>
          pre_fork: <function Prefork.pre_fork at 0x7fed60cd81f0>
          post_fork: <function Postfork.post_fork at 0x7fed60cd8310>
          post_worker_init: <function PostWorkerInit.post_worker_init at 0x7fed60cd8430>
          worker_int: <function WorkerInt.worker_int at 0x7fed60cd8550>
          worker_abort: <function WorkerAbort.worker_abort at 0x7fed60cd8670>
          pre_exec: <function PreExec.pre_exec at 0x7fed60cd8790>
          pre_request: <function PreRequest.pre_request at 0x7fed60cd88b0>
          post_request: <function PostRequest.post_request at 0x7fed60cd8940>
          child_exit: <function ChildExit.child_exit at 0x7fed60cd8a60>
          worker_exit: <function WorkerExit.worker_exit at 0x7fed60cd8b80>
          nworkers_changed: <function NumWorkersChanged.nworkers_changed at 0x7fed60cd8ca0>
          on_exit: <function OnExit.on_exit at 0x7fed60cd8dc0>
          proxy_protocol: False
          proxy_allow_ips: ['127.0.0.1']
          keyfile: None
          certfile: None
          ssl_version: 2
          cert_reqs: 0
          ca_certs: None
          suppress_ragged_eofs: True
          do_handshake_on_connect: False
          ciphers: None
          raw_paste_global_conf: []
          strip_header_spaces: False
        [2022-11-25 00:20:41 +0100] [13821] [INFO] Starting gunicorn 20.1.0
        [2022-11-25 00:20:41 +0100] [13821] [DEBUG] Arbiter booted
        [2022-11-25 00:20:41 +0100] [13821] [INFO] Listening at: unix:/home/doelf/bin/blauen/run/gunicorn.sock (13821)
        [2022-11-25 00:20:41 +0100] [13821] [INFO] Using worker: sync
        [2022-11-25 00:20:41 +0100] [13824] [INFO] Booting worker with pid: 13824
        [2022-11-25 00:20:41 +0100] [13825] [INFO] Booting worker with pid: 13825
        [2022-11-25 00:20:41 +0100] [13826] [INFO] Booting worker with pid: 13826
        [2022-11-25 00:20:41 +0100] [13821] [DEBUG] 3 workers
    



# Konfigurieren von NGINX

## Source

https://medium.com/analytics-vidhya/dajngo-with-nginx-gunicorn-aaf8431dc9e0
https://mattsegal.dev/nginx-django-reverse-proxy-config.html

Matt's Dev Blog: https://mattsegal.dev/

Each Nginx virtual server should be described by a file in the /etc/nginx/sites-available directory. You select which sites you want to enable by making symbolic links to those in the /etc/nginx/sites-enabled directory.

By default, there is only one conf file named default that has a basic setup for NGINX. You can either modify it or create a new one. In our case, I am going to delete it:

        sudo rm -rf /etc/nginx/sites-available/default
        sudo rm -rf /etc/nginx/sites-enabled/default

Es wird eine neues Nginx Server Konfigurationsfile mit dem name blauen erstellt, und zwar im Verzeichnis /etc/nginx/sites-available.

Es hat folgenden Inhalt:

        upstream http://127.0.0.1:8000 {
                # fail_timeout=0 means we always retry an upstream even if it failed
                # to return a good HTTP response (in case the Unicorn master nukes a
                # single worker for timing out).
                server unix:/home/ubuntu/hello_django/run/gunicorn.sock fail_timeout=0;
        }
        
        server {
                # Listen on port 80 for incoming requests.
                listen   80;
                server_name neptun.fritz.box;
                # location = /favicon.ico { access_log off; log_not_found off; }
                #client_max_body_size 4G;
                #access_log /home/doelf/bin/blauen/logs/nginx-access.log;
                #error_log /home/doelf/bin/blauen/logs/nginx-error.log;
        
        
                location /forbidden {
                        return 403;
                }
        
                location /static/ {
                        alias /home/doelf/bin/blauen/dproject/staticfiles/;
                }
        
                location /media/ {
                        root   /home/doelf/bin/media/;
                }
        
                location / {
                        proxy_pass http://127.0.0.1:8000;
                        # Ensure original Host header is forwarded to our Django app.
                        proxy_set_header Host $host;
                        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                        proxy_set_header X-Forwarded-Proto $scheme;
                        proxy_redirect http://127.0.0.1:8000 http://neptun.fritz.box;
                }
        }
        

Es muss noch ein symbolischer Link erstellt werden:

        sudo ln -s /etc/nginx/sites-available/blauen /etc/nginx/sites-enabled/blauen


##  Status Nginx


        (blauen) doelf@neptun:/etc/nginx/sites-enabled$ sudo service nginx statuts
        Usage: nginx {start|stop|restart|reload|force-reload|status|configtest|rotate|upgrade}
        (blauen) doelf@neptun:/etc/nginx/sites-enabled$ sudo service nginx status
        ● nginx.service - A high performance web server and a reverse proxy server
             Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
             Active: active (running) since Thu 2022-11-24 13:51:55 CET; 17s ago
               Docs: man:nginx(8)
            Process: 5742 ExecStartPre=/usr/sbin/nginx -t -q -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
            Process: 5743 ExecStart=/usr/sbin/nginx -g daemon on; master_process on; (code=exited, status=0/SUCCESS)
           Main PID: 5744 (nginx)
              Tasks: 5 (limit: 9297)
             Memory: 4.8M
                CPU: 26ms
             CGroup: /system.slice/nginx.service
                     ├─5744 "nginx: master process /usr/sbin/nginx -g daemon on; master_process on;"
                     ├─5745 "nginx: worker process" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" >
                     ├─5746 "nginx: worker process" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" >
                     ├─5747 "nginx: worker process" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" >
                     └─5748 "nginx: worker process" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" "" >
        
        Nov 24 13:51:55 neptun systemd[1]: Starting A high performance web server and a reverse proxy server...
        Nov 24 13:51:55 neptun systemd[1]: Started A high performance web server and a reverse proxy server.


doelf@neptun:~$ sudo systemctl restart nginx
doelf@neptun:~$ sudo vim  /etc/nginx/sites-enabled/blauen 
doelf@neptun:~$ sudo systemctl daemon-reload
doelf@neptun:~$ sudo systemctl restart nginx


# Set Up Ubuntu To Serve A Django Website Step By Step

Source https://simpleit.rocks/python/django/set-up-ubuntu-to-serve-a-django-website-step-by-step/

