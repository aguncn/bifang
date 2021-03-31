#!/bin/sh

function  start_gunicorn(){
        gunicorn -c gunicorn_conf.py bifangback.wsgi:application
}

function  stop_gunicorn(){
        ps aux | grep gunicorn | grep -v grep | awk 'NR==1{system("kill -QUIT "$2)}'
}

function  reload_gunicorn(){
        ps aux | grep gunicorn | grep -v grep | awk 'NR>1{system("kill -HUP "$2)}'
}

case $1 in
  start)
        start_gunicorn;;
  stop)
        stop_gunicorn;;
  reload)
        reload_gunicorn;;
  *)
        echo "Usage:`basename $0` {start|stop|reload}";;
esac