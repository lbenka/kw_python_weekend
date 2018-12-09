import os
from datetime import datetime
from pathlib import Path

import flask
from flask.json import jsonify

from lb.modules.alsa import get_routes


app = flask.Flask(__name__, template_folder=str(Path(os.path.dirname(__file__)).parent / "templates"))


@app.route("/search")
def search():
    return flask.render_template("front_page.html")


@app.route("/results")
def get_routes_from_site():
    print(1)
    src = flask.request.args.get("src")
    dst = flask.request.args.get("dst")
    when = flask.request.args.get("when")

    when_parsed = datetime.strptime(when, "%Y/%m/%d")
    routes = get_routes(src, dst, when_parsed)
    return jsonify(routes)
