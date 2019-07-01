import click
from datetime import datetime, timedelta

from lb.modules.fetch import fetch_provider


@click.command()
@click.option("--src", prompt="Source of trip", help="From where you wanna start your trip.")
@click.option("--dst", prompt="Destination of trip", help="To where you wanna go")
@click.option("--when", prompt="When", help="When you wanna leave")
def click_routes(src, dst, when):
    when_parsed = datetime.strptime(when, "%Y/%m/%d")
    provider_class = fetch_provider("regiojet")
    routes = provider_class().get_routes(
        source=src, destination=dst, departure=when_parsed, arrival=when_parsed + timedelta(days=1)
    )
    click.echo(routes)


if __name__ == "__main__":
    """CLI using click library to make our life easier."""
    click_routes()
