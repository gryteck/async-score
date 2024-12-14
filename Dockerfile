FROM python:3.11-slim as base
WORKDIR /
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir
COPY .env .
ENV PYTHONPATH=/

COPY entrypoint.sh /
COPY ./src /src

# RUN chmod +x /enrtypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

