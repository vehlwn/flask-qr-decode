#!/bin/sh

export SECRET_KEY="${FLASK_SECRET_KEY}"
export FLASK_RUN_PORT="${FLASK_INTERNAL_PORT}"
export FLASK_ENV="production"
export FLASK_RUN_HOST="0.0.0.0"
export FLASK_APP="main.py"
export FLASK_CONFIG="docker"
export FLASK_HASH_INITIAL_VALUE="$(od --address-radix n --read-bytes 4 --format u /dev/urandom)"

while true; do
    flask deploy
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done

gunicorn --workers=16 --bind=0.0.0.0:$GUNICORN_INTERNAL_PORT main:app
