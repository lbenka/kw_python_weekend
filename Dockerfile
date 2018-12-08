FROM benkalukas/py_weekend_base

WORKDIR /app

COPY Pipfile* /app/

RUN pipenv install --system --deploy

COPY . /app

CMD [ "gunicorn", "lb.journey_finder_flask.api:app"]

# debug 
# EXPOSE 5000
# ENV FLASK_APP="lb.journey_finder_flask.api:app"
# CMD ["flask", "run", "--host=0.0.0.0"]
