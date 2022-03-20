FROM python:3.10-slim-buster

WORKDIR /

COPY requirements.txt requirements.txt

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

RUN pip install -r requirements.txt

COPY . .

CMD ["python3",  "-O", "start.py"]
