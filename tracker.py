#!/usr/bin/python
import os
from elixir import *
from model import *

def start(filename="custom.hike"):
	metadata.bind = "sqlite:///" + filename # connect
	options_defaults['tablename'] = lambda c: c.__name__.lower()
	setup_all()
	if not os.path.exists(filename):
		create_all()

save = session.commit
