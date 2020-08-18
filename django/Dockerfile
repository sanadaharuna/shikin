FROM python:3.8.5-alpine3.11
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip
ADD requirements.txt /code/
RUN apk add --update --no-cache mariadb-connector-c-dev \
    && apk add --no-cache --virtual .build-deps \
    mariadb-dev \
    gcc \
    musl-dev \
    build-base \
    linux-headers\
    && pip install -r requirements.txt \
    && apk del .build-deps \
    && apk add tzdata
