import click
from datetime import datetime
from alsa import get_routes

@click.command()
@click.option('--src', prompt='Source of trip', help='From where you wanna start your trip.')
@click.option('--dst', prompt='Destination of trip', help='To where you wanna go')
@click.option('--when', prompt='When', help='When you wanna leave')
def cli_routes(src, dst, when):
    when_parsed = datetime.strptime(when, "%Y/%m/%d")
    routes = get_routes(src, dst, when_parsed)
    click.echo(routes)

if __name__ == '__main__':
    """CLI using click library to make our life easier."""
    cli_routes()