#!/bin/bash

export FLASK_ENV=development
export FLASK_DEBUG=1

python3 /server/manage.py

exec "$@"
