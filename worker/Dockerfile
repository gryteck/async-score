FROM python:3.11-slim as base
WORKDIR /

COPY worker/requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY worker/src worker/src

COPY worker/entrypoint.sh /
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]