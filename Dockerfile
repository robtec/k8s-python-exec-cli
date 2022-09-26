FROM python:3.9-alpine

ADD . /app

WORKDIR /app

RUN pip3 install -r requirements.txt