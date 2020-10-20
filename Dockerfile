FROM python:3.8-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

COPY Pipfile Pipfile.lock ./

RUN apk update \
    && pip install pipenv \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pipenv install --deploy --system \
    && apk del build-deps

COPY . .

RUN adduser -D runuser
USER runuser

CMD gunicorn car_makes.wsgi:application --bind 0.0.0.0:$PORT
