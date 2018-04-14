#!/bin/bash

python3 /server/manage.py deploy

exec "$@"
