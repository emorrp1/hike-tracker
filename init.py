#!/usr/bin/python
# python-setuptools, python-sqlite, easy_install Elixir
from elixir import *
from model import *

metadata.bind = "sqlite:///custom.hike" # connect
#metadata.bind.echo = True # display all SQL queries
options_defaults['tablename'] = lambda c: c.__name__.lower()

setup_all(True) # setup internal repr, then create database
