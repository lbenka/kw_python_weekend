import os
from datetime import datetime, timedelta
from pathlib import Path

from flask import Blueprint, render_template, request
from flask.json import jsonify

from lb.modules.fetch import fetch_provider


flask_search = Blueprint(
    "flask_search", __name__, template_folder=str(Path(os.path.dirname(__file__)).parent / "templates")
)


@flask_search.route("/search")
def search():
    return render_template("front_page.html")


@flask_search.route("/results")
def get_routes_from_site():
    print(1)
    src = request.args.get("src")
    dst = request.args.get("dst")
    when = request.args.get("when")

    when_parsed = datetime.strptime(when, "%Y/%m/%d")
    provider_class = fetch_provider('regiojet')
    routes = provider_class().get_routes(
        source=src, destination=dst, departure=when_parsed, arrival=when_parsed + timedelta(days=1)
    )
    return jsonify(routes)
