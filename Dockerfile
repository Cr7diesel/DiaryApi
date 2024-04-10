FROM python:3.10-alpine3.19

ENV PYTHONUNBUFFERED=1

WORKDIR /diary_api

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN apk add postgresql-client build-base postgresql-dev
RUN pip install -r requirements.txt
RUN adduser --disabled-password admin

USER admin

COPY . /diary_api

EXPOSE 8000