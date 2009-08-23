#!/usr/bin/python -iW ignore::DeprecationWarning
import elixir
import model

def start(hike='custom'):
	'''Start the database connection, creating the tables and configuring if necessary'''
	from os.path import exists, expanduser
	hike = expanduser(hike + '.hike')
	elixir.metadata.bind = 'sqlite:///%s' % hike
	elixir.setup_all()
	if exists(hike):
		model.Config.store()
	else:
		from convert import load
		elixir.create_all()
		hike = hike.replace('.hike', '.conf')
		load(hike)

def save():
	model.Config.store()
	elixir.session.commit()

def set_distances(config):
	'''Set the distances between bases'''
	if 'routes' in config:
		for r in config['routes']:
			ds = config['routes'][r]
			route = model.Route.get(r)
			for i in range(len(ds)):
				d = ds[i]
				base,next = route.bases[i:i+2]
				base._set_distance(next, d)
		del config['routes']
	for b1 in config:
		base = model.Base.get(b1)
		for b2d in config[b1]:
			b2,d = b2d.split(':')
			other = model.Base.get(b2)
			base._set_distance(other, d)

def all(type):
	'''Shortcut to a list of specified hike objects'''
	types = {'b':model.Base, 'r':model.Route, 't':model.Team}
	t = type[0].lower()
	return types[t].query.all()

def get(tname):
	'''Shortcut to getting hike objects by name'''
	type = tname[0].lower()
	name = tname[1:]
	types = {'b':model.Base, 'r':model.Route, 't':model.Team}
	return types[type].get(name)

def get_all(type=None):
	'''Load all objects into global namespace'''
	types = {'b':model.Base, 'r':model.Route, 't':model.Team}
	if type:
		t = type[0].lower()
		for i in all(t):
			tname = t + i.name
			line = '%s = get("%s")' % (tname, tname)
			exec line in globals()
	else:
		for t in types:
			get_all(t)
