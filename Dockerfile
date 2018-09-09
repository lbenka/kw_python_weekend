FROM python:3.6-alpine

WORKDIR /app
COPY . /app

RUN apk add --update --no-cache g++ gcc libxslt-dev

RUN pip install pipenv 
RUN pipenv install --system --deploy --verbose

EXPOSE 8000

CMD [ "hug", "-f", "/app/api.py" ]