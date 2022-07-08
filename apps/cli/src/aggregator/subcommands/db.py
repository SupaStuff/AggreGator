import click

from .helpers.init_db import init_db

@click.group()
def db():
  pass

@db.command()
def init():
  """Create the Timescale DB with AggreGator (hyper)tables"""
  init_db()
