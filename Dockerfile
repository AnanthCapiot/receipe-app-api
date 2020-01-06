FROM python:3.7-alpine

MAINTAINER Capiot Software Ltd

ENV PYTHONUNBUFFERED 1

copy ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# -- create new user
RUN adduser -D user

# -- Run as user (instead of root account)
USER user
