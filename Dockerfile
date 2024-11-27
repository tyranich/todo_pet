FROM python:3.11-alpine

COPY ./todo /usr/src/app/

WORKDIR /usr/src/app/todo/

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt



