# filename: happy_birthday.py
"""A basic (single function) API written using hug"""
import hug
from datetime import datetime, timedelta
from jinja2 import FileSystemLoader, Environment

from lb.modules.fetch import fetch_provider
from lb.journey_finder_hug.template_engine import get_template

template_engine = Environment(loader=FileSystemLoader("templates"))


@hug.get("/search", output=hug.output_format.html)
def show_ui():
    template = get_template("front_page.html")
    return template.render()


@hug.cli()
@hug.get("/results")
def get_routes_from_site(src, dst, when, provider):
    when_parsed = datetime.strptime(when, "%Y/%m/%d")
    provider_class = fetch_provider(provider)
    routes = provider_class().get_routes(
        source=src, destination=dst, departure=when_parsed, arrival=when_parsed + timedelta(days=1)
    )
    return routes
