YouTube MP3 Converter - YTBmp3.com
========================

A Django web application for extracting the audio from a YouTube video and converts it to MP3 that a user can download.

**Live Site:** https://www.ytbmp3.com
and for video **Live Site:** https://www.ytbmp4.com

Main aplication made by https://github.com/jcalazan/youtube-audio-dl 
In this aplication corrected same bugs.
MP3 files are corupted (can't play in same players) in original application (corrected)
MP3 quality setted to 134Kbs and can bee changed apps/downloader/tasks.py#77


----------------
YTBmp3 now is  now much improved. Story about tehnology will be soon. 
**Story about development:** https://orangeunit.com/projects/youtube-mp3-converter/

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
```
virtualenv /srv/first
cd /sr/first
source bin/activate
pip install Django
git clone https://github.com/mishop/ytbmp3.git
pip install requirments.txt
```
setup your domain and database
/settings/base.py
```
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
    #redirect non-www to www
}
```

uwsgi configuration
---------
read more
http://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html
```
# mysite_uwsgi.ini file
[uwsgi]

# Django-related settings
# the base directory (full path)
chdir           = /srv/first/ytbmp3
# Django's wsgi file
module          = ytbmp3.wsgi
# the virtualenv (full path)
home            = /srv/first/
#logto		= /srv/first/ytbmp3/error.log
# process-related settings
# master
master          = true
# maximum number of worker processes
processes       = 4
max-requests	= 3000
# the socket (use the full path to be safe
socket          = /srv/first/ytbmp3/ytbmp3.sock
# ... with appropriate permissions - may be needed
 chmod-socket    = 664
# clear environment on exit
vacuum          = true
```

