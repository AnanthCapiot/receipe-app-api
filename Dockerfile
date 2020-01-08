FROM python:3.7-alpine

MAINTAINER Capiot Software Ltd

ENV PYTHONUNBUFFERED 1

copy ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
       gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# -- create new user
RUN adduser -D user

# -- Run as user (instead of root account)
USER user
