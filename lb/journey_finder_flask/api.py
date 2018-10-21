import flask

from lb.modules.alsa import get_routes

app = flask.Flask(__name__, template_folder="/app/lb/templates")

@app.route('/search')
def search():
    return flask.render_template("front_page.html")

@app.route('/results')
def get_routes_from_site(src, dst, when):
    when_parsed = datetime.strptime(when, "%Y/%m/%d")
    routes = get_routes(src, dst, when_parsed)
    return routes