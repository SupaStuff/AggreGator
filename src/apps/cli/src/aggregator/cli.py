import click

from .subcommands.db import db
from .subcommands.market import market

if __name__ == '__main__':
    cli = click.CommandCollection(sources=[db, market])
    cli()
