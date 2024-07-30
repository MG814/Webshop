#!/bin/sh

until cd /app/src
do
    echo "Waiting for server volume..."
done

# run a worker
celery -A core worker --loglevel=info -E --pool=solo