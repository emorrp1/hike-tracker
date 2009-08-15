#!/usr/bin/python -iW ignore::DeprecationWarning
import elixir
import model

def start(hike='custom'):
	'''Start the database connection, creating the tables and configuring if necessary'''
	from os.path import exists
	hike += '.hike'
	elixir.metadata.bind = 'sqlite:///%s' % hike
	elixir.setup_all()
	if not exists(hike):
		elixir.create_all()
		configure(hike[:-5])
		save()

save = elixir.session.commit

def configure(hike='custom'):
	'''Create the hike definition if the config exists'''
	from os.path import exists
	hike += '.conf'
	if exists(hike):
		from configobj import ConfigObj
		config = ConfigObj(hike)
		if 'start' in config:
			s = config['start']
			model.START = model.mkdt(s[-5:], s[:-5])
		if 'wiggle' in config:
			model.Base.wfact = float(config['wiggle'])
		if 'bases' in config:
			for b in config['bases']:
				model.Base(b, config['bases'][b])
			if 'routes' in config:
				for r in config['routes']:
					model.Route(r, config['routes'][r])
		if 'teams' in config:
			for t in config['teams']:
				model.Team(t, *config['teams'][t])
		if 'distances' in config:
			if 'routes' in config['distances'] and 'routes' not in config:
				config['distances'].pop('routes')
			set_distances(config['distances'])

def set_distances(config):
	'''Set the distances between bases'''
	if 'routes' in config:
		for r in config['routes']:
			ds = config['routes'][r]
			route = model.Route.get_by(name=r)
			for i in range(len(ds)):
				d = ds[i]
				base,next = route.bases[i:i+2]
				model.Base.set_distance(base.name, next.name, d)
		del config['routes']
	for b1 in config:
		for b2d in config[b1]:
			b2,d = b2d.split(':')
			model.Base.set_distance(b1, b2, d)

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
	return types[type].get_by(name=name)

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
