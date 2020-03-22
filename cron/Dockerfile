FROM alpine:latest

RUN \
    apk add --no-cache curl tzdata && \
    cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    apk del tzdata

RUN mkdir -p /var/spool/cron/crontabs
COPY ./root /var/spool/cron/crontabs/root

CMD busybox crond -l 2 -L /dev/stderr -f