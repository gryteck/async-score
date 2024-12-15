#!/bin/bash

alembic upgrade head

gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.main:app -b 0.0.0.0:81 --forwarded-allow-ips "*" --proxy-allow-from "*" --proxy-protocol