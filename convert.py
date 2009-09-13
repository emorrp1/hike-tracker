#!/usr/bin/python -W ignore::DeprecationWarning
import elixir
import model
from configobj import ConfigObj

def save(config):
	config = ConfigObj(config)
	config['config'] = {}
	for k in model.Config.default:
		config['config'][k] = model.Config.to_v[k](model.Config[k])
	bs = model.Base.query.all()
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
		rs = model.Route.query.all()
		if rs:
			config['routes'] = {}
			for r in rs:
				config['routes'][r.name] = []
				for b in r.bases:
					config['routes'][r.name].append(b.name)
	ts = model.Team.query.all()
	if ts:
		config['teams'] = {}
		for t in ts:
			time = t.start.strftime('%H:%M')
			config['teams'][t.name] = [t.route.name, time]
	config.write()

def load(hike):
	'''Create the hike definition if the config exists'''
	config = ConfigObj(hike)
	if 'config' in config:
		c = config['config']
		for k in model.Config.default:
			if k in c:
				model.Config[k] = model.Config.from_v[k](c[k])
			else:
				model.Config[k] = None
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
			st = model.Config['start'] + offset - int(first)*interval
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

if __name__ == '__main__':
	from sys import argv
	if len(argv) == 2:
		config = argv[1]
		if '.conf' in config:
			hike = config.replace('.conf', '.hike')
		else:
			hike = config + '.hike'
		dest = None
	else:
		hike = argv[1]
		dest = argv[2]
	elixir.metadata.bind = 'sqlite:///%s' % hike
	elixir.setup_all()
	if dest:
		save(dest)
	else:
		elixir.create_all()
		load(config)
