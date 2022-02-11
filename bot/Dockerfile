# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /

COPY requirements.txt requirements.txt

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

RUN pip3 install -r requirements.txt

COPY . .

CMD python3 -OO start.py
