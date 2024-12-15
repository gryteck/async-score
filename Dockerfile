FROM python:3.11-slim as base
WORKDIR /
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir
COPY alembic.ini .
COPY .env .
ENV PYTHONPATH=/

COPY entrypoint.sh /
COPY /postgres/migrations /postgres/migrations
COPY ./src /src

RUN chmod +x /entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

