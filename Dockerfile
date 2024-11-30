FROM python:3.11-alpine

WORKDIR /usr/src/app/todo/

COPY ./requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./todo /usr/src/app/

COPY ./entrypoint.sh /entrypoint.sh

