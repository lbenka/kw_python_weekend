# filename: happy_birthday.py
"""A basic (single function) API written using hug"""
import hug
from datetime import datetime
from jinja2 import FileSystemLoader, Environment

from lb.modules.alsa import get_routes
from lb.journey_finder_hug.template_engine import get_template

template_engine = Environment(loader=FileSystemLoader("templates"))


@hug.get("/search", output=hug.output_format.html)
def show_ui():
    template = get_template("front_page.html")
    return template.render()


@hug.cli()
@hug.get("/results")
def get_routes_from_site(src, dst, when):
    when_parsed = datetime.strptime(when, "%Y/%m/%d")
    routes = get_routes(src, dst, when_parsed)
    return routes
