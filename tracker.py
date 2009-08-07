#!/usr/bin/python -iW ignore::DeprecationWarning
from elixir import *
import model
from configobj import ConfigObj
from os.path import exists

def start(hike='custom'):
	'''Start the database connection, creating the tables and configuring if necessary'''
	hike += '.hike'
	metadata.bind = 'sqlite:///%s' % hike
	setup_all()
	if not exists(hike):
		create_all()
		configure(hike[:-5])
		save()

save = session.commit

def configure(hike='custom'):
	'''Create the hike definition if the config exists'''
	hike += '.conf'
	if exists(hike):
		config = ConfigObj(hike)
		for b in config['bases']:
			model.Base(b, config['bases'][b])
		for r in config['routes']:
			model.Route(r, config['routes'][r])
		for t in config['teams']:
			model.Team(t, *config['teams'][t])

def get(tname):
	'''Shortcut to getting hike objects by name'''
	type = tname[0].lower()
	name = tname[1:]
	types = {'b':model.Base, 'r':model.Route, 't':model.Team}
	return types[type].get_by(name=name)

def get_all(type=None):
	'''Load all objects into global namespace'''
	types = {'b':model.Base, 'r':model.Route, 't':model.Team}
	if type:
		t = type[0].lower()
		for i in types[t].query.all():
			tname = t + i.name
			line = '%s = get("%s")' % (tname, tname)
			exec line in globals()
	else:
		for t in types:
			get_all(t)
