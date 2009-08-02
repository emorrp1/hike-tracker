#!/usr/bin/python -iW ignore::DeprecationWarning
from elixir import *
from model import *

def start(hike="custom"):
	hike += ".hike"
	from os.path import exists
	metadata.bind = "sqlite:///%s" % hike
	setup_all()
	if not exists(hike):
		create_all()

save = session.commit
