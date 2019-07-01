from flask import Flask


def create_app():
    app = Flask(__name__)

    from lb.journey_finder_flask.api import flask_search
    app.register_blueprint(flask_search)

    return app
