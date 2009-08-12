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
		for b in config['bases']:
			model.Base(b, config['bases'][b])
		for r in config['routes']:
			model.Route(r, config['routes'][r])
		for t in config['teams']:
			model.Team(t, *config['teams'][t])
		if 'distances' in config:
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
				b1, b2 = base.name, next.name
				if b1 not in model.Base.distances:
					model.Base.distances[b1] = {}
				if b2 not in model.Base.distances:
					model.Base.distances[b2] = {}
				model.Base.distances[b1][b2] = int(d)
				model.Base.distances[b2][b1] = int(d)
		del config['routes']
	for b1 in config:
		if b1 not in model.Base.distances:
			model.Base.distances[b1] = {}
		for b2d in config[b1]:
			b2,d = b2d.split(':')
			if b2 not in model.Base.distances:
				model.Base.distances[b2] = {}
			model.Base.distances[b1][b2] = int(d)
			model.Base.distances[b2][b1] = int(d)

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
