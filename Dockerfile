FROM python:3.5

WORKDIR /srv/app

COPY ./requirements.txt /srv/app/

RUN pip install -r requirements.txt
