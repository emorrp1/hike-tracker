#!/usr/bin/python
import os
from elixir import *
from model import *

def start(filename="custom.hike"):
	metadata.bind = "sqlite:///" + filename # connect
	if os.path.exists(os.path.abspath(filename)):
		setup_all()
	else:
		options_defaults['tablename'] = lambda c: c.__name__.lower()
		setup_all(True)

save = session.commit
