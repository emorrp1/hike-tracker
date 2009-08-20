#!/usr/bin/python -W ignore::DeprecationWarning
import elixir
import model
from configobj import ConfigObj

def save(config):
	config = ConfigObj(config)
	config['start'] = model.Config.get_by(key='start').value
	config['wiggle'] = model.Config.get_by(key='wfact').value
	config['figs'] = model.Config.get_by(key='figs').value
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
	from os.path import exists, expanduser
	from configobj import ConfigObj
	config = ConfigObj(hike)
	if 'start' in config:
		s = config['start']
		model.config['start'] = model.mkdt(s[-5:], s[:-5])
	if 'wiggle' in config:
		model.config['wfact'] = float(config['wiggle'])
	if 'figs' in config:
		model.config['figs'] = int(config['figs'])//2
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
			st = model.config['start'] + offset - int(first)*interval
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
	model.Config.store()
	elixir.session.commit()

if __name__ == '__main__':
	from sys import argv
	elixir.metadata.bind = 'sqlite:///%s' % argv[1]
	elixir.setup_all()
	save(argv[2])
