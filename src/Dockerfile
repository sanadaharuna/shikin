FROM python:3.8.2-alpine3.11
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN apk add --update --no-cache mariadb-connector-c-dev \
    && apk add --no-cache --virtual .build-deps \
    mariadb-dev \
    gcc \
    musl-dev \
    build-base \
    linux-headers\
    && pip install mysqlclient==1.4.6 \
    uwsgi==2.0.18 \
    && apk del .build-deps

RUN pip install --upgrade pip
ADD requirements.txt /code/
RUN pip install -r requirements.txt
