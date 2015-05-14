YouTube MP3 Downloader
========================

A Django web application for extracting the audio from a YouTube video and converts it to MP3 that a user can download.

**Live Site:** http://www.ytbmp3.com
Main aplication made by https://github.com/jcalazan/youtube-audio-dl 
In this aplication corrected same bugs.
MP3 files are corupted (can't play in same players) in original application (corrected)
MP3 quality setted to 134Kbs and can bee changed apps/downloader/tasks.py#77

Technology Stack
----------------

- Python 2.7
- Django 1.9
- Twitter Bootstrap 3
- PostgreSQL
- Nginx
- Gunicorn
- Celery
- RabbitMQ
- Supervisor
- Virtualenv
- ffmpeg or avconv
- memcached
- python-memcache

Instalation
-----------
setup your domain and database
/settings/base.py
```
virtualenv /srv/first
cd /sr/first
source bin/activate
pip install Django
git clone http://github.com/mishop/
pip install requirments.txt
python manage.py migrate
python manage.py collectstatic
```

Nginx conf
---------
```
# the upstream component nginx needs to connect to
upstream django {
     server unix:///srv/first/ytbmp3/ytbmp3.sock; # for a file socket
   # server 127.0.0.1:8001; # for a web port socket (we'll use this first)
}

# configuration of the server
server {
    # the port your site will be served on
    listen      80;
    # the domain name it will serve for
    server_name www.ytbmp3.com; # setup your domain
    charset     utf-8;
    
    root /srv/first/ytbmp3/ytbmp3/;
    # max upload size
    client_max_body_size 75M;   # adjust to taste

    # Django media
    location /media  {
        alias /srv/first/ytbmp3/ytbmp3/media;  # your Django project's media files - amend as required
    }

    location /static {
        alias /srv/first/ytbmp3/ytbmp3/collected_static; # your Django project's static files - amend as required
    }
   
    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include     /srv/first/ytbmp3/uwsgi_params; # the uwsgi_params file you installed
    }
}
server {
    listen       80;
    server_name  ytbmp3.com;
    return       301 http://www.ytbmp3.com$request_uri;
}
```

uwsgi configuration
read more
http://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html
---------
```
# mysite_uwsgi.ini file
[uwsgi]

# Django-related settings
# the base directory (full path)
chdir           = /first/first/ytbmp3
# Django's wsgi file
module          = ytbmp3.wsgi
# the virtualenv (full path)
home            = /first/first/
#logto		= /first/first/ytbmp3/error.log
# process-related settings
# master
master          = true
# maximum number of worker processes
processes       = 4
max-requests	= 3000
# the socket (use the full path to be safe
socket          = /first/first/ytbmp3/ytbmp3.sock
# ... with appropriate permissions - may be needed
 chmod-socket    = 664
# clear environment on exit
vacuum          = true
```
