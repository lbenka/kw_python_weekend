FROM python:3.7-alpine3.8

WORKDIR /app

RUN apk add --update --no-cache g++ gcc libxslt-dev 

COPY Pipfile* /app/

RUN pip install --upgrade pip
RUN pip install pipenv 
RUN pipenv install --system --deploy --verbose

# you should probably change this 
# EXPOSE 8000
# CMD [ "hug", "-f", "lb/journey_finder_hug/start_up/hug_api.py" ]

COPY . /app

EXPOSE 5000
ENV FLASK_APP="lb.journey_finder_flask.api:app"
CMD ["flask", "run", "--host=0.0.0.0"]