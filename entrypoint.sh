#!/bin/bash
set -e
uwsgi --http 0.0.0.0:8008 --pythonpath src --wsgi-file app.wsgi  --enable-threads --disable-logging --master --processes 1 --threads 2 --stats :9001 --stats-http --http-timeout 900 --ini uwsgi.ini
