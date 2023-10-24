#!/bin/sh
touch /app/uwsgi.sock

# Start uWSGI
uwsgi --ini /app/app.ini &

# Start Nginx in the foreground
nginx -g "daemon off;"