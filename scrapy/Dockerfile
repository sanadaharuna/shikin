FROM python:3.8.3-alpine3.11
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN apk add --update --no-cache mariadb-connector-c-dev \
    && apk add --no-cache --virtual .build-deps \
    mariadb-dev \
    gcc \
    musl-dev \
    build-base \
    linux-headers\
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
    && pip install mysqlclient==1.4.6 
ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN apk del .build-deps
RUN apk add libxslt tzdata
ENV TZ=Asia/Tokyo
COPY crontab /var/spool/cron/crontabs/root
CMD ["crond", "-f", "-L", "/dev/stderr"]
