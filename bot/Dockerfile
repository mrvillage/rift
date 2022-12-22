# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /

COPY requirements.txt requirements.txt

RUN apt-get clean && \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git gcc net-tools

RUN pip3 install -r requirements.txt

COPY . .

CMD export DOCKER_HOST_IP=$(route -n | awk '/UG[ \t]/{print $2}') && python3 -OO start.py
