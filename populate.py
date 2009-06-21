#!/usr/bin/python
from elixir import *
from model import *
from datetime import datetime

metadata.bind = "sqlite:///custom.hike" # connect

setup_all()

home = Location(e=000,n=000)
noon = datetime(2009,06,22,12,00)
home_noon = Event(time=noon,loc=home)
team = Team(number=101)
team.seen.append(home_noon)

session.commit()
