# todo: Base image that I prepared for you 
FROM benkalukas/py_weekend_base
# todo: set app as working directory, this is standard in the industry 
WORKDIR /app
# todo: Copy Pipfile into cantainer
COPY Pipfile* /app/
# todo: Install all the required packages from Pipfile into container system python  
RUN pipenv install --system --deploy
# todo: here I am copying all the files into container
COPY . /app
# todo: gunicorn is python package that you need to install
CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "lb.journey_finder_flask.entrypoint:create_app()"]

# todo: docker build -t py_weekend 
# todo: docker run -p 8000:8000 py_weekend
# todo: open site: localhost:8000/your_path_defined_in_flask