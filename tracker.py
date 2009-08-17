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

def save(config=False):
	elixir.session.commit()
	if config:
		from configobj import ConfigObj
		config += '.conf'
		config = ConfigObj(config)
		config['start'] = model.START.strftime('%y%m%d%H:%M')
		config['wiggle'] = model.Base.wfact
		bs = all('bases')
		if bs:
			config['bases'] = {}
			if model.Distance.query.all():
				config['distances'] = {}
			for b in bs:
				config['bases'][b.name] = b.ref()
				ds = model.Distance.query.filter_by(start=b)
				if ds.count():
					config['distances'][b.name] = []
					for d in ds:
						item = '%s:%d' % (d.end.name, d.distance)
						config['distances'][b.name].append(item)
			rs = all('routes')
			if rs:
				config['routes'] = {}
				for r in rs:
					config['routes'][r.name] = []
					for b in r.bases:
						config['routes'][r.name].append(b.name)
		ts = all('teams')
		if ts:
			config['teams'] = {}
			for t in ts:
				time = t.start.strftime('%H:%M')
				config['teams'][t.name] = [t.route.name, time]
		config.write()

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
			if 'distances' in config:
				if 'routes' in config['distances'] and 'routes' not in config:
					config['distances'].pop('routes')
				set_distances(config['distances'])
		if 'teams' in config:
			c = config['teams']
			def auto(route, prefix, first, last, interval=None, offset=0):
				from datetime import timedelta
				if not interval:
					interval = 5
				interval = timedelta(minutes=int(interval))
				offset = timedelta(minutes=int(offset))
				st = model.START + offset - int(first)*interval
				for i in range(int(first),int(last)+1):
					start = st + i*interval
					name = prefix + str(i).rjust(2,'0')
					model.Team(name, route, start.time())
			if 'routes' in c:
				if 'routes' in config:
					for r in c['routes']:
						auto(r, *c['routes'][r])
				c.pop('routes')
			for t in c:
				model.Team(t, *c[t])

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
