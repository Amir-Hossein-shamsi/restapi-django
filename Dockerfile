FROM python:3.10.4-slim-bullseye

LABEL maintainer="AmirHossein"
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY  ./requirements.txt  /requirements.txt
RUN pip install -r /requirements.txt
RUN mkdir /app
WORKDIR /app

COPY . /app/

RUN adduser --disabled-password  user
USER user