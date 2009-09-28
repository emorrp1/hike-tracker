#!/usr/bin/python -W ignore::DeprecationWarning
from model import *
from configobj import ConfigObj

def save(config):
	config = ConfigObj(config)
	config['config'] = {}
	config['config']['wfact'] = conf().wfact
	config['config']['start'] = conf().start.strftime('%y%m%d%H:%M')
	config['config']['naith'] = conf().naith
	config['config']['figs']  = conf().figs
	bs = Base.query.all()
	if bs:
		config['bases'] = {}
		for b in bs:
			config['bases'][b.name] = [b.ref(), b.h]
	rs = Route.query.all()
	if rs:
		config['routes'] = {}
		for r in rs:
			config['routes'][r.name] = []
			for b in r.bases:
				config['routes'][r.name].append(b.name)
	ls = Leg.query.all()
	if ls:
		config['legs'] = {}
		for l in ls:
			id = '-'.join([l.start.name, l.end.name])
			config['legs'][id] = [l.dist, l.gain]
	ts = Team.query.all()
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
		if 'start' in c:
			start = c['start']
			conf().start = mkdt(start[-5:], start[:-5])
		if 'wfact' in c: conf().wfact = float(c['wfact'])
		if 'naith' in c: conf().naith = float(c['naith'])
		if 'figs'  in c: conf().figs  = int(c['figs'])
	if 'bases' in config:
		for b in config['bases']:
			Base(b, *config['bases'][b])
	if 'routes' in config:
		for r in config['routes']:
			Route(r, config['routes'][r])
	if 'legs' in config:
		c = config['legs']
		def auto(route, *dgs):
			route = Route.get(route)
			for i in range(len(dgs)):
				dg = dgs[i].split('/')
				d = dg[0]
				if len(dg) == 2: g = dg[1]
				else: g = None
				base, next = route.bases[i:i+2]
				Leg.set(base, next, d, g)
		if 'routes' in c:
			if 'routes' in config:
				for r in c['routes']:
					auto(r, *c['routes'][r])
			c.pop('routes')
		for l in c:
			start, end = l.split('-')
			Leg.set(start, end, *c[l])
	if 'teams' in config:
		c = config['teams']
		def auto(route, prefix, first, last, interval=None, offset=0):
			from datetime import timedelta
			if not interval:
				interval = 5
			interval = timedelta(minutes=int(interval))
			offset = timedelta(minutes=int(offset))
			st = conf().start + offset - int(first)*interval
			for i in range(int(first),int(last)+1):
				start = st + i*interval
				name = prefix + str(i).rjust(2,'0')
				Team(name, route, start.time())
		if 'routes' in c:
			if 'routes' in config:
				for r in c['routes']:
					auto(r, *c['routes'][r])
			c.pop('routes')
		for t in c:
			Team(t, *c[t])
	db.session.commit()

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
	db.metadata.bind = 'sqlite:///%s' % hike
	db.setup_all()
	if dest:
		save(dest)
	else:
		db.create_all()
		load(config)
