#!/bin/sh
#

export FLASK_APP=/root/src/main.py

if ! /bin/nc -w 5 -z localhost 6379;then
    /usr/local/bin/redis-server >/dev/null 2>&1 &
fi
flask run --host 0.0.0.0 --port 80
