#!/usr/bin/python -iW ignore::DeprecationWarning
from elixir import *
from model import *
from configobj import ConfigObj
from os.path import exists

def start(hike="custom"):
	hike += ".hike"
	metadata.bind = "sqlite:///%s" % hike
	setup_all()
	if not exists(hike):
		create_all()

save = session.commit

def configure(hike="custom"):
	hike += ".conf"
	if exists(hike):
		config = ConfigObj(hike)
		for b in config['bases']:
			Base(b, config['bases'][b])
		for r in config['routes']:
			Route(r, config['routes'][r])
		for t in config['teams']:
			Team(t, config['teams'][t])
