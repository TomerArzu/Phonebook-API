#FROM ubuntu
FROM python:3.10-slim-buster

LABEL image="phone-book"

WORKDIR /opt/success_flight

RUN apt-get update
RUN mkdir -p /opt/PhoneBook
COPY . /opt/PhoneBook

RUN  apt-get update && apt-get install -y
RUN pip install --no-cache-dir -r /opt/PhoneBook/requirements.txt

ENV PYTHONUNBUFFERED 1

EXPOSE 5000

ENTRYPOINT FLASK_APP=/opt/PhoneBook/main.py flask run --host=0.0.0.0 --port 5000