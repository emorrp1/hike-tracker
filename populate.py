#!/usr/bin/python
from elixir import *
from model import *

metadata.bind = "sqlite:///custom.hike" # connect

home = Location(e=000,n=000,t=0)
alpha = Base(name="Alpha",e=010,n=010,t=4)

phil = Steward(name="Philip",role="base assistant")
cec = Steward(name="Cecelia",role="base leader")
phil.base = alpha
cec.base = alpha

senior = Route(section="senior")
t = Team(number=101)
clare = Participant(name="Clare")
clare.team = t
clare.team.route = senior
clare.team.location = home

senior.bases = [alpha]

session.commit()
