FROM python:3.7-alpine

RUN apk add --update --no-cache g++ gcc libxslt-dev postgresql-dev python3-dev musl-dev

COPY Pipfile* /

RUN pip install --upgrade pip
RUN pip install pipenv 
RUN pipenv install --system --deploy --verbose
